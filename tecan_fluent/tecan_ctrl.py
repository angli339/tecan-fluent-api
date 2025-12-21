import sys
import clr
sys.path.append("C:/Program Files (x86)/Tecan/FluentControl")
clr.AddReference('Tecan.VisionX.API.V2')

import threading
import Tecan.VisionX.API.V2 as api

from .command_elements_liha import *
from .command_elements_mca import *

def build_command(cmd_object: ET.Element) -> api.Commands.GenericCommand:
    el = ScriptGroup([cmd_object])
    ET.indent(el)
    cmd = api.Commands.GenericCommand()
    cmd.set_Content(ET.tostring(el, encoding='unicode'))
    return cmd

class Tecan():
    def __init__(self) -> None:
        self.fc = api.FluentControl()
        if not self.fc.IsRunning():
            raise RuntimeError("FluentControl is not running")

        self.fc.StartOrAttach()
        self.rt = self.fc.GetRuntime()

        self.ch = None
        self.event_ch_open = threading.Event()
        def Runtime_ChannelOpens(openChannel: api.IExecutionChannel):
            self.ch = openChannel
            print("Channel %s is open" % self.ch.Channel)
            self.event_ch_open.set()
        ch_opens = api.ChannelChange(Runtime_ChannelOpens)
        m_add_ChannelOpens = self.rt.GetType().GetMethod("add_ChannelOpens")
        m_add_ChannelOpens.Invoke(self.rt, [ch_opens])
    
    def wait_channel(self) -> None:
        self.event_ch_open.wait()

    def run_command(self, cmd: api.Commands.ICommand) -> None:
        if self.ch is None:
            raise RuntimeError("API channel is not open")
        self.ch.ExecuteCommand(cmd)

    def add_labware(self, label: str, type: str,
                    location: str, position: int,
                    rotation: int = 0) -> None:
        cmd = api.Commands.AddLabware(label, type, location, rotation, position)
        self.run_command(cmd)
    
    def liha_get_tips(self,
                      i_selected_tips: list[int],
                      diti_type: str,
                      use_next_position: bool=True,
                      airgap_volume: int=10,
                      airgap_speed: int=70):
        cmd = build_command(Object_LihaGetTipsScriptCommandDataV3(
            i_selected_tips=i_selected_tips,
            diti_type=diti_type,
            use_next_position=use_next_position,
            airgap_volume=airgap_volume,
            airgap_speed=airgap_speed
        ))
        self.run_command(cmd)

    def liha_drop_tips(self,
                       i_selected_tips: list[int],
                       diti_waste: str = 'MCA Thru Deck Waste Chute_1',
                       skip_if_nothing_mounted: bool=True):
        cmd = build_command(Object_LihaDropTipsScriptCommandDataV2(
            i_selected_tips=i_selected_tips,
            diti_waste=diti_waste,
            skip_if_nothing_mounted=skip_if_nothing_mounted
        ))
        self.run_command(cmd)
    
    def liha_set_tips_back(self,
                           i_selected_tips: list[int], 
                           labware: str,
                           i_selected_wells: list[int]):
        cmd = build_command(Object_LihaSetTipsBackScriptCommandDataV1(
            i_selected_tips=i_selected_tips,
            labware=labware,
            i_selected_wells=i_selected_wells
        ))
        self.run_command(cmd)
    
    def liha_aspirate(self,
                      volumes: list[int],
                      i_selected_tips: list[int],
                      labware: str, i_selected_wells: list[int],
                      liquid_class: str,
                      is_switch_container_source_enabled: bool=False):
        cmd = build_command(Object_LihaAspirateScriptCommandDataV5(
            volumes=volumes,
            i_selected_tips=i_selected_tips,
            labware=labware,
            i_selected_wells=i_selected_wells,
            liquid_class=liquid_class,
            is_switch_container_source_enabled=is_switch_container_source_enabled
        ))
        self.run_command(cmd)
    
    def liha_dispense(self,
                      volumes: list[int],
                      i_selected_tips: list[int],
                      labware: str, i_selected_wells: list[int],
                      liquid_class: str):
        cmd = build_command(LihaDispenseScriptCommandDataV4(
            volumes=volumes,
            i_selected_tips=i_selected_tips,
            labware=labware,
            i_selected_wells=i_selected_wells,
            liquid_class=liquid_class
        ))
        self.run_command(cmd)
    
    def liha_mix(self,
                 n_cycles: int,
                 volumes: list[int],
                 i_selected_tips: list[int],
                 labware: str, i_selected_wells: list[int],
                 liquid_class: str):
        cmd = build_command(Object_LihaMixScriptCommandDataV4(
            n_cycles=n_cycles,
            volumes=volumes,
            i_selected_tips=i_selected_tips,
            i_selected_wells=i_selected_wells,
            labware=labware,
            liquid_class=liquid_class
        ))
        self.run_command(cmd)

    def mca_get_head_adapter(self, head_adapter="EVA[001]", air_gap_volume: int = 0):
        cmd = build_command(Object_Mca384GetHeadAdapterScriptCommandDataV1(
            head_adapter=head_adapter,
            air_gap_volume=air_gap_volume
        ))
        self.run_command(cmd)

    def mca_get_tips(self,
                     labware: str,
                     air_gap_volume: int = 0,
                     adapterplate: str = 'EVA',
                     first_tip_pos_xy: tuple[int, int] = (1, 1),
                     last_tip_pos_xy: tuple[int, int] = (12, 8)):
        
        cmd = build_command(Object_Mca384GetTipsScriptCommandDataV1(
            labware=labware,
            air_gap_volume=air_gap_volume,
            adapterplate=adapterplate,
            first_tip_pos_xy=first_tip_pos_xy,
            last_tip_pos_xy=last_tip_pos_xy,
        ))
        self.run_command(cmd)
    
    def mca_aspirate(self, volume: float, labware: str, liquid_class: str):
        cmd = build_command(Object_Mca384AspirateScriptCommandDataV2(
            volume=volume,
            labware=labware,
            liquid_class=liquid_class,
        ))
        self.run_command(cmd)

    def mca_dispense(self, volume: float, labware: str, liquid_class: str):
        cmd = build_command(Object_Mca384DispenseScriptCommandDataV2(
            volume=volume,
            labware=labware,
            liquid_class=liquid_class,
        ))
        self.run_command(cmd)

    def mca_drop_tips(self, diti_waste: str = 'MCA Thru Deck Waste Chute_1'):
        cmd = build_command(Object_Mca384DropTipsScriptCommandDataV1(
            back_position='BackToPosition',
            labware=diti_waste,
        ))
        self.run_command(cmd)

    def mca_drop_tips_back_to_source(self):
        cmd = build_command(Object_Mca384DropTipsScriptCommandDataV1(
            back_position='BackToSource',
            labware='',
        ))
        self.run_command(cmd)
