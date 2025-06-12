from google.adk.agents import Agent

from .tools import create_vertexai_image
from .sub_agents import create_tiktok_coordinator_agent, create_image_prompt_loop_agent, video_generator_loop_agent

from . import instructions


root_agent = Agent(
    model='gemini-2.0-flash',
    # model='gemini-2.0-flash-live-preview-04-09', # for live preview - audio etc.
    name='smm_content_creator',
    description='''
    An orchestrator agent running a group of sub-agents with the ultimate goal of creating an engaging,
    fun and smm-focused content for various platforms (like TikTok, Instagram, etc.).
    ''',
    instruction=instructions.COORDINATOR_AGENT_INSTRUCTIONS,
    sub_agents=[create_tiktok_coordinator_agent(), create_image_prompt_loop_agent(), video_generator_loop_agent],
    # tools=[create_vertexai_image],
    # after_agent_callback=read_write_google_sheet
)