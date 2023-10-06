import json
from abc import ABC

class BaseState(ABC):
    pass

# Exception for undefined transitions in the FSM
class UndefinedTransition(Exception):
    def __init__(self, state, input):
        self.message = f"Undefined transition ({state.__class__.__name__}, {input})"
        super().__init__(self.message)

# Read settings from a JSON file
def read_settings(filename):
    with open(filename, "r") as file:
        settings = json.load(file)
    return settings

# Create state instances based on the settings
def create_states(settings):
    states = {}
    for state_info in settings["states"]:
        state_name = state_info["name"]
        state_output = state_info["output"]
        state_transitions = dict()

        for transition in state_info["transitions"]:
            state_transitions[transition["with"]] = transition["to"]

        new_state = type(state_name, (BaseState,), {"output": state_output, "transitions" : state_transitions})()
        states[state_name] = new_state
    return states

class FSM:
    def __init__(self, states, initial_state):
        self.states = states
        self.current_state = initial_state  # Set current state to initial state
        print(self.current_state.output)  # Do something in the initial state

    def toggle(self, input):
        if input in self.current_state.transitions:
            next_state_name = self.current_state.transitions[input]
            next_state = self.states[next_state_name]  # Get the next state object
            self.current_state = next_state  # Change state
            print(self.current_state.output)  # Do something after changing state
        else:
            raise UndefinedTransition(self.current_state, input)

if __name__ == "__main__":
    settings = read_settings("states_settings.json")
    states = create_states(settings)
    initial_state = states["StartScreen"]

    fsm = FSM(states, initial_state)

    while True:
        user_input = input()
        fsm.toggle(user_input)