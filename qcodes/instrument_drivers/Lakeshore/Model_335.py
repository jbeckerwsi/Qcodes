from typing import ClassVar, Dict, Any
import pyvisa as visa

import qcodes.utils.validators as vals
from qcodes.instrument.group_parameter import GroupParameter, Group

from .lakeshore_base import LakeshoreBase, BaseOutput, BaseSensorChannel
from .Lakeshore_model_336 import LakeshoreModel336Channel as Model_336_Channel
from .Lakeshore_model_336 import (
    LakeshoreModel336CurrentSource as Output_336_CurrentSource,
)

# There are 4 sensors channels (a.k.a. measurement inputs) in Model 336.
# Unlike other Lakeshore models, Model 336 refers to the channels using
# letters, and not numbers
_channel_name_to_command_map: Dict[str, str] = {'A': 'A',
                                                'B': 'B'}

class LakeshoreModel335(LakeshoreBase):
    """
    Lakeshore Model 335 Temperature Controller Driver
    """
    channel_name_command: Dict[str, str] = _channel_name_to_command_map

    CHANNEL_CLASS = Model_336_Channel

    input_channel_parameter_values_to_channel_name_on_instrument = \
        _channel_name_to_command_map

    def __init__(self, name: str, address: str, **kwargs) -> None:
        super().__init__(name, address, **kwargs)

        if isinstance(self.visa_handle,visa.resources.serial.SerialInstrument):
            self.visa_handle.baud_rate = 57600
            self.visa_handle.data_bits = 7
            self.visa_handle.parity = visa.constants.Parity(1)

        self.output_1 = Output_336_CurrentSource(self, 'output_1', 1)
        self.output_2 = Output_336_CurrentSource(self, 'output_2', 2)
