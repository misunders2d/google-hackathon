from google.adk.agents import Agent, LoopAgent, SequentialAgent
from google.adk.tools import google_search, load_web_page
from google.adk.tools import exit_loop
from . import instructions

MODEL='gemini-2.0-flash'


#--- checker agent creating functions
def create_fact_checker():
    fact_checker_agent = Agent(
        name=instructions.FACT_CHECKER_AGENT,
        model=MODEL,
        description='An agent meticulously checking facts from a given text. Uses web search to search for information',
        instruction=instructions.FACT_CHECK_AGENT_INSTRUCTIONS,
        tools=[google_search],
        output_key='fact_checker_corrections'
    )
    return fact_checker_agent

#--- ideas generation 
def create_ideas_agent():
    ideas_agent = Agent(
        name='ideas_generator',
        model=MODEL,
        description='An agent generating engaging ideas for TikTok posts from a given topic. The ideas are suitable for TikTok',
        instruction=instructions.IDEA_CREATOR_INSTRUCTIONS,
        tools=[exit_loop],
        output_key=instructions.INITIAL_IDEAS_KEY,
    )
    return ideas_agent

def create_ideas_loop_agent():
    ideas_loop_agent = LoopAgent(
        name=instructions.IDEA_CREATOR,
        description='An agent that generates ideas for TikTok posts and checks facts in this content using google search',
        sub_agents=[create_ideas_agent(), create_fact_checker()],
        max_iterations=7
    )
    return ideas_loop_agent

#--- text content creation
def create_text_content_agent():
    text_content_drafter_agent = Agent(
        name='text_content_drafter',
        model=MODEL,
        description='An agent who creates extended content based on the provided idea',
        instruction=instructions.TEXT_CONTENT_AGENT_INSTRUCTIONS,
        tools=[exit_loop],
        output_key=instructions.STORY_TEXT_KEY
    )
    return text_content_drafter_agent

def create_text_content_loop_agent():
    text_content_loop_agent = LoopAgent(
        name=instructions.CONTENT_CREATOR,
        description='An agent that creates text content based on the approved idea and checks facts in this content using google search',
        sub_agents=[create_text_content_agent(), create_fact_checker()],
        max_iterations=7
    )
    return text_content_loop_agent

#--- image ideas generation
def create_image_ideas_agent():
    image_ideas_agent = Agent(
        name='image_ideas_creator',
        model=MODEL,
        description='An agent who creates ideas for images based on the presented text content',
        instruction=instructions.IMAGE_IDEAS_AGENT_INSTRUCTIONS,
        tools=[exit_loop],
        output_key=instructions.IMAGE_IDEAS_KEY
    )
    return image_ideas_agent

def create_image_ideas_checker():
    image_ideas_checker_agent = Agent(
        name=instructions.IMAGE_IDEAS_CHECKER,
        model=MODEL,
        description='An agent checking image ideas and making sure they accurately reflect the essence of the text content provided',
        instruction=instructions.IMAGE_IDEAS_CHECKER_INSTRUCTIONS,
        tools=[google_search],
        output_key='image_ideas_checker_corrections'
    )
    return image_ideas_checker_agent

def create_image_ideas_loop_agent():
    image_ideas_loop_agent = LoopAgent(
        name=instructions.IMAGE_IDEAS_CREATOR,
        description='An agent that creates image ideas based on the provided text content and picks the best matching ideas for image creation',
        sub_agents=[create_image_ideas_agent(), create_image_ideas_checker()],
        max_iterations=7
    )
    return image_ideas_loop_agent

#--- image prompt generation
def create_image_prompt_generator_agent():
    image_prompt_generator_agent = Agent(
        name='image_prompt_generator',
        model=MODEL,
        description='An agent who creates rich, detailed prompts for image generation',
        instruction=instructions.IMAGE_PROMPT_AGENT_INSTRUCTIONS,
        tools=[exit_loop],
        output_key=instructions.IMAGE_PROMPTS_KEY
    )
    return image_prompt_generator_agent

def create_image_prompt_checker():
    image_prompt_checker_agent = Agent(
        name=instructions.IMAGE_PROMPTS_CHECKER,
        model=MODEL,
        description='An agent who is an expert in image generation and can check presented prompts for inconsistencies or flaws, and suggest improvements',
        instruction=instructions.IMAGE_PROMPT_CHECKER_INSTRUCTIONS,
        output_key='image_prompt_checker_corrections'
    )
    return image_prompt_checker_agent

def create_image_prompt_loop_agent():
    image_prompt_loop_agent = LoopAgent(
        name=instructions.IMAGE_PROMPTS_CREATOR,
        description='An agent that creates rich image-generation prompts',
        sub_agents=[create_image_prompt_generator_agent(), create_image_prompt_checker()],
        max_iterations=7
    )
    return image_prompt_loop_agent

def create_content_summarizer_agent():
    summarizer_agent = Agent(
        name='summarizer_agent',
        model=MODEL,
        description='Agent that gathers the content creation data',
        instruction=instructions.SUMMARIZER_INSTRUCTIONS
    )
    return summarizer_agent

def create_full_cycle_content_agent():
    tik_tok_creator = SequentialAgent(
        name='tiktok_content_creator_agent',
        description="An agent running full cycle of TikTok content creation from a pre-approved idea, including text content and image generation",
        sub_agents=[
            create_text_content_loop_agent(),
            create_image_ideas_loop_agent(),
            create_image_prompt_loop_agent(),
            create_content_summarizer_agent()
        ]
    )
    return tik_tok_creator

def create_tiktok_coordinator_agent():
    tiktok_coordinator = Agent(
        name='tiktok_master',
        description='An agent running full cycle of TikTok content creation, from initial idea generation to text content and image generation',
        model=MODEL,
        instruction=(
            "You are a main point of contact with the user, who wants to create content for TikTok. "
            "Your job is to understand the user's goal and idea. Ask the user additional questions if you don't understand what they want. "
            f"If you understand the user's main idea, you MUST use {instructions.IDEA_CREATOR} agent to help users generate ideas. "
            "This is where you MUST explicitly ask the user whether they approve any of the suggestions, or they want you to generate more ideas. "
            "ONLY if the user has a specific idea or has approved some of yur suggestions, you may pass the conversation to `tiktok_content_creator_agent`"
            ),
        sub_agents=[create_ideas_loop_agent(), create_full_cycle_content_agent()]
    )
    return tiktok_coordinator

video_generation_drafter=Agent(
    name='video_prompts_drafter_agent',
    description='An agent which drafts prompts for video generation models',
    instruction=instructions.VIDEO_GENERATION_GUIDELINES,
    tools=[exit_loop],
    output_key=instructions.VIDEO_PROMPTS_KEY
)

video_prompt_checker=Agent(
    name=instructions.VIDEO_PROMPTS_CHECKER,
    description='An agent who is an expert in video prompts and checsk the submitted prompts for errors and completeness',
    instruction=instructions.VIDEO_PROMPT_CHECKER_INSTRUCTIONS,
    tools=[load_web_page.load_web_page]
)

video_generator_loop_agent = LoopAgent(
    name=instructions.VIDEO_PROMPTS_CREATOR,
    description='An agent that creates rich video-generation prompts',
    sub_agents=[video_generation_drafter, video_prompt_checker],
    max_iterations=7
)