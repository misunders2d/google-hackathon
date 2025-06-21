from google.adk.agents import Agent

from .sub_agents import create_tiktok_coordinator_agent, create_image_prompt_loop_agent

from . import instructions


def create_root_agent():
    root_agent = Agent(
        model='gemini-2.0-flash',
        name='smm_content_creator',
        description='''
        An orchestrator agent running a group of sub-agents with the ultimate goal of creating an engaging,
        fun and smm-focused content for various platforms (like TikTok, Instagram, etc.).
        ''',
        instruction=instructions.COORDINATOR_AGENT_INSTRUCTIONS,
        sub_agents=[create_tiktok_coordinator_agent(), create_image_prompt_loop_agent()],
    )
    return root_agent
