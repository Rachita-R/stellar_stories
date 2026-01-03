import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- Stories data ---
stories = {
    "astronaut": {
        "title": "Aurora's Call from the International Space Station",
        "intro": "Commander Sarah Chen watches Earth's aurora from the ISS as a solar storm approaches...",
        "scenarios": [
            {
                "text": "The space station's radiation detectors start beeping urgently. What do you do?",
                "choices": [
                    {"text": "Check the Aurora monitoring systems", "outcome": "You discover the solar storm is creating spectacular auroras but also dangerous radiation levels."},
                    {"text": "Contact Mission Control immediately", "outcome": "Mission Control confirms a major geomagnetic storm and advises shelter protocols."}
                ]
            },
            {
                "text": "The aurora intensifies, creating a breathtaking light show. How do you respond?",
                "choices": [
                    {"text": "Document the phenomenon for research", "outcome": "Your photos help scientists understand space weather patterns."},
                    {"text": "Focus on crew safety protocols", "outcome": "You successfully protect the crew from radiation exposure."}
                ]
            }
        ]
    },
    "farmer": {
        "title": "The Day the Sky Touched the Farm",
        "intro": "Miguel tends his crops in rural Argentina when the GPS systems start malfunctioning...",
        "scenarios": [
            {
                "text": "Your precision farming equipment stops working due to GPS interference. What's your next move?",
                "choices": [
                    {"text": "Switch to manual farming methods", "outcome": "You maintain crop care using traditional techniques your grandfather taught you."},
                    {"text": "Wait for GPS to restore", "outcome": "You lose valuable planting time but learn about space weather impacts."}
                ]
            },
            {
                "text": "Strange lights appear in the southern sky. How do you react?",
                "choices": [
                    {"text": "Research the phenomenon", "outcome": "You discover you're witnessing a rare aurora at low latitudes due to a geomagnetic storm."},
                    {"text": "Check on your animals", "outcome": "Your animals are restless, sensing the electromagnetic disturbance."}
                ]
            }
        ]
    },
    "pilot": {
        "title": "Navigating the Solar Storm",
        "intro": "Captain Elena Volkov faces communication blackouts during a polar route flight...",
        "scenarios": [
            {
                "text": "Radio communications cut out over the Arctic. What's your priority?",
                "choices": [
                    {"text": "Change altitude to restore communications", "outcome": "You successfully find a communication window at a lower altitude."},
                    {"text": "Continue on current flight path", "outcome": "You rely on backup navigation systems and maintain passenger safety."}
                ]
            },
            {
                "text": "Passengers notice unusual aurora displays. How do you handle this?",
                "choices": [
                    {"text": "Make an announcement about the phenomenon", "outcome": "Passengers are delighted to witness this rare natural display."},
                    {"text": "Focus on flight safety monitoring", "outcome": "You ensure all systems remain operational despite electromagnetic interference."}
                ]
            }
        ]
    }
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/story/<character>')
def story(character):
    if character in stories:
        story_data = stories[character]
        story_json = json.dumps(story_data)   # convert to JSON string
        return render_template('result.html',
                               character=character,
                               story=story_data,
                               story_json=story_json)
    return "Story not found", 404


@app.route('/api/choice', methods=['POST'])
def handle_choice():
    data = request.json
    character = data.get('character')
    scenario_index = int(data.get('scenario', -1))
    choice_index = int(data.get('choice', -1))

    if character in stories and 0 <= scenario_index < len(stories[character]['scenarios']):
        scenario = stories[character]['scenarios'][scenario_index]
        if 0 <= choice_index < len(scenario['choices']):
            choice = scenario['choices'][choice_index]
            return jsonify({
                'outcome': choice['outcome'],
                'next_scenario': scenario_index + 1 if scenario_index + 1 < len(stories[character]['scenarios']) else None
            })

    return jsonify({'error': 'Invalid choice'}), 400


if __name__ == '__main__':
    app.run(debug=True)
