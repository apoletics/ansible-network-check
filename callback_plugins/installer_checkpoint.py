"""Ansible callback plugin to print a summary completion status of installation
phases.
"""
from datetime import datetime
from ansible.plugins.callback import CallbackBase
from ansible import constants as C


class CallbackModule(CallbackBase):
    """This callback summarizes installation phase status."""

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'installer_checkpoint'
    CALLBACK_NEEDS_WHITELIST = False

    def __init__(self):
        super(CallbackModule, self).__init__()

    def v2_playbook_on_stats(self, stats):

        # Return if there are no custom stats to process
        if stats.custom == {}:
            return

        phases = stats.custom['_run']

        ordered_phases = sorted(phases, key=lambda x: (phases[x].get('from', ''),phases[x].get('to', ''),phases[x].get('protocol', ''), phases[x].get('port', ''), phases[x].get('result', '') ))

        self._display.banner('NETWORK CHECK REPORT')
        # Display status information for each phase
        for phase in ordered_phases:
            phase_protocol = str(phases[phase].get('protocol', '')).upper()
            phase_from = phases[phase].get('from', '')
            phase_to = phases[phase].get('to', '')
            phase_port = phases[phase].get('port', '')
            phase_result = phases[phase].get('result', '')
            if phase_protocol:
                self._display.display(
                    'FROM:{}, TO:{}, PROT:{}, PORT:{}, RESULT:{} '.format(phase_from, phase_to,phase_protocol, phase_port, phase_result),color=self.phase_color(phase_result))

    def phase_color(self, status):
        """ Return color code for installer phase"""
        valid_status = [
            'FAILED',
            'OK',
        ]

        if status not in valid_status:
            self._display.warning('Invalid phase status defined: {}'.format(status))

        if status == 'OK':
            phase_color = C.COLOR_OK
        elif status == 'FAILED':
            phase_color = C.COLOR_ERROR
        else:
            phase_color = C.COLOR_WARN

        return phase_color
