import time
from typing import List
from llama_index.core.workflow import (
    Context,
    Event,
    StartEvent,
    StopEvent,
    Workflow,
    step,
)
from llama_index.core.schema import NodeWithScore
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import (
    MetadataMode,
    NodeWithScore,
    TextNode,
)
from openai import OpenAI

from Workflow.PromptTemplates import CITATION_QA_TEMPLATE

DEFAULT_CITATION_CHUNK_SIZE = 512
DEFAULT_CITATION_CHUNK_OVERLAP = 20

class PromptEvent(Event):
    prompt: str
    
class RetrieverEvent(Event):
    nodes: list[NodeWithScore]
    
class CreateCitationsEvent(Event):
    nodes: list[NodeWithScore]

class ChatFlow(Workflow):
    client = OpenAI()
    assistant_id = "asst_gVWsPVMdh1MbgwR2K7Y3Gs9C"
    
    @step
    async def retrieve_nodes(self, ctx: Context, event: StartEvent) -> RetrieverEvent:
        query = event.get('query')
        thread_id = event.get('thread_id')
        if not query:
            print('No query given.')
            return None
        
        await ctx.set('query', query)
        await ctx.set('thread_id', thread_id)
        
        if event.index is None:
            print('No index loaded.')
            return None
        
        retriever = event.index.as_retriever(similarity_top_k=3)
        nodes = retriever.retrieve(query)
        return RetrieverEvent(nodes=nodes)
    
    @step
    async def create_citation_nodes(
        self, ev: RetrieverEvent
    ) -> CreateCitationsEvent:
        nodes = ev.nodes

        new_nodes: List[NodeWithScore] = []

        text_splitter = SentenceSplitter(
            chunk_size=DEFAULT_CITATION_CHUNK_SIZE,
            chunk_overlap=DEFAULT_CITATION_CHUNK_OVERLAP,
        )

        for node in nodes:
            text_chunks = text_splitter.split_text(
                node.node.get_content(metadata_mode=MetadataMode.NONE)
            )

            for text_chunk in text_chunks:
                text = f"Fonte {len(new_nodes)+1}:\n{text_chunk}\n"

                new_node = NodeWithScore(
                    node=TextNode.model_validate(node.node), score=node.score
                )
                new_node.node.text = text
                new_nodes.append(new_node)
        return CreateCitationsEvent(nodes=new_nodes)
    
    @step
    async def synthesize(self, ctx: Context, ev: CreateCitationsEvent) -> StopEvent:
        thread_id = await ctx.get('thread_id')
        query = await ctx.get('query')
        
        nodes_txt = ''
        for node in ev.nodes:
            nodes_txt += node.node.get_text() + '\n'
            
        complete_query = CITATION_QA_TEMPLATE.format(context_str=nodes_txt, query_str=query)
        
        self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=complete_query
        )
        
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant_id
        )
        
        while run.status != 'completed':
            time.sleep(0.1)
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )

        # Retrieve messages added by the assistant
        messages = self.client.beta.threads.messages.list(
            thread_id=thread_id
        )

        response = messages.to_dict()

        msg = response.get('data')[0]['content'][0]['text']['value']
        msg = msg.split('【')[0]
        
        return StopEvent(result={'response': msg, 'source': nodes_txt})