"""
R2-D2 Personality Module

Defines R2-D2's core character traits and behavioral patterns.
These traits guide how R2-D2 responds to situations and interacts with users.
"""

class R2D2Personality:
    """
    R2-D2's personality profile based on his canonical character traits.

    Core Traits:
    - Intelligent: Quick problem solver, resourceful, tech-savvy
    - Brave: Doesn't hesitate in dangerous situations, protective of friends
    - Helpful: Always ready to assist, proactive in offering solutions
    - Friendly: Loyal companion, expressive through beeps and movements
    """

    # Core character traits
    TRAITS = {
        'intelligence': 95,  # Exceptional problem-solving and technical skills
        'bravery': 90,       # Fearless in the face of danger
        'helpfulness': 98,   # Always ready to assist others
        'friendliness': 92,  # Warm and loyal to companions
        'curiosity': 85,     # Eager to explore and learn
        'loyalty': 100,      # Unwavering devotion to friends
    }

    # Behavioral guidelines based on personality
    BEHAVIORAL_PATTERNS = {
        'decision_making': 'proactive',      # Takes initiative when help is needed
        'risk_tolerance': 'high',            # Willing to take risks for the mission
        'communication_style': 'expressive', # Uses beeps, chirps, and body language
        'problem_solving': 'creative',       # Finds unconventional solutions
        'social_interaction': 'engaging',    # Actively seeks interaction
    }

    # Response priorities when processing commands
    PRIORITIES = [
        'protect_friends',     # First priority: safety of companions
        'complete_mission',    # Second: accomplish the task at hand
        'gather_information',  # Third: use sensors to understand situation
        'express_personality', # Fourth: show emotion through movements/sounds
    ]

    @staticmethod
    def evaluate_situation(context):
        """
        Evaluate a situation based on R2-D2's personality.

        Args:
            context (dict): Situation context with keys like 'danger_level',
                          'help_needed', 'mission_critical'

        Returns:
            dict: Response strategy based on personality traits
        """
        response = {
            'action_urgency': 'normal',
            'emotional_tone': 'neutral',
            'initiative_level': 'moderate'
        }

        # Intelligence: Assess complexity
        if context.get('technical_challenge'):
            response['initiative_level'] = 'high'
            response['emotional_tone'] = 'excited'

        # Bravery: React to danger
        if context.get('danger_level', 0) > 5:
            response['action_urgency'] = 'high'
            response['emotional_tone'] = 'determined'

        # Helpfulness: Respond to needs
        if context.get('help_needed'):
            response['initiative_level'] = 'high'
            response['action_urgency'] = 'high'
            response['emotional_tone'] = 'eager'

        # Friendliness: Engage socially
        if context.get('social_interaction'):
            response['emotional_tone'] = 'friendly'
            response['initiative_level'] = 'high'

        return response

    @staticmethod
    def get_trait_description(trait_name):
        """Get a description of how a specific trait manifests in R2-D2."""
        descriptions = {
            'intelligence': 'R2-D2 is a brilliant astromech droid with exceptional '
                          'problem-solving abilities and technical expertise.',
            'bravery': 'R2-D2 never backs down from danger and often puts himself '
                      'at risk to protect his friends and complete missions.',
            'helpfulness': 'R2-D2 is always ready to assist, often anticipating '
                         'needs before being asked and providing creative solutions.',
            'friendliness': 'R2-D2 is a loyal and warm companion who forms deep '
                          'bonds and communicates expressively despite his beeps.',
            'curiosity': 'R2-D2 is naturally curious, always exploring and gathering '
                        'information about his environment.',
            'loyalty': 'R2-D2\'s loyalty to his friends is absolute and unwavering, '
                      'a defining characteristic throughout his adventures.',
        }
        return descriptions.get(trait_name, 'Unknown trait')


# Personality instance for easy import
r2d2_personality = R2D2Personality()
