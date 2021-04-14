from stmpy import Machine

class ClientMachine():

    def __init__(self, driver, audio_recorder, audio_player, mqtt, name="stm"):
        # Setup state machine
        self.name = name
        self.state_machine = Machine(
            name=self.name, 
            transitions=self.get_transitions(), 
            states=self.get_states(), 
            obj=self
        )
        driver.add_machine(self.state_machine)

        # Setup references
        self.audio_recorder = audio_recorder
        self.audio_player = audio_player
        self.mqtt = mqtt

    
    def get_transitions(self):
        return [
            {'source': 'initial', 'target': 'ready'},
            {'trigger': 'start', 'source': 'ready', 'target': 'recording'},
            {'trigger': 'done', 'source': 'recording', 'target': 'ready'},
        ]
    
    def get_states(self):
        return [
            {'name': 'ready'},
            {'name': 'recording', 'do': 'record()', "stop": "stop_recording()"},
        ]
    
    def record(self):
        self.audio_recorder.record()

    def stop_recording(self):
        self.audio_recorder.stop()


