# Copyright 2019-2023 NVIDIA CORPORATION

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import omni.ext
import omni.ui as ui
import omni.usd
import asyncio
from typing import List
from .robotmotion import RobotMotion
from .mqtt_csv_client import MQTTData
omni.kit.pipapi.install("pxr")
from pxr import Usd
import os
import time




# Functions and vars are available to other extension as usual in python: `example.python_ext.some_public_function(x)`
def some_public_function(x: int):
    print(f"[omni.hello.world] some_public_function was called with {x}")
    return x ** x


# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class MyExtension(omni.ext.IExt):
    motions: List[RobotMotion] = [None, None, None, None]
    filename = str(os.environ['CSV_FILE']) 
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[omni.hello.world] MyExtension startup")
        # self.show_window(True)
        # omni.usd.Stage.Open(str(os.environ['OV_DEFAULT_STAGE_LOAD']))
        self._count = 0       
        self._window = ui.Window("My Window", width=300, height=300)
        with self._window.frame:
            with ui.VStack():
                label = ui.Label("")
                

                def on_click():
                    self._count += 1
                    label.text = f"count: {self._count}"

                def on_reset():
                    self._count = 0
                    label.text = "empty"

                on_reset()

                with ui.HStack():
                    ui.Button("Add", clicked_fn=on_click)
                    ui.Button("Reset", clicked_fn=on_reset)
        MQTTData.read_csv()

    # def show_window(self, toggled):
    #     if toggled:
    #         if self._window is None:
    #             self._window = MsftKhiAnimationWindow()
    #             self._window.set_visibility_changed_fn(self._visiblity_changed_fn)
    #         else:
    #             self._window.show()
    #     else:
    #         if self._window is not None:
    #             self._window.hide()

    def on_shutdown(self):
        print("[omni.hello.world] MyExtension shutdown")

    def _move_click(self):
        # if self.motion is None:
        # self.motion = RobotMotion('/World/khi_rs007n_vac_UNIT1/world_003/base_link_003',
        #                           ['link1piv_003', 'link2piv_003', 'link3piv_003', 'link4piv_003',
        #                            'link5piv_003', 'link6piv_003'])

        if self.motions[0] is not None and self.motions[0].animating:
            self.motions[0].stopAnimating()

            return

        self.motions[0] = RobotMotion('/World/PCR_8FT2_Only_Robot/khi_rs007n_vac_UNIT1/world_003/base_link_003',
                                      ['link1piv_003', 'link2piv_003', 'link3piv_003', 'link4piv_003',
                                       'link5piv_003', 'link6piv_003'])
       
        asyncio.ensure_future(self.motions[0].startAnimating())

    def _move_csv_data(self):
     
          
        self.motions[0] = RobotMotion('/World/PCR_8FT2_Only_Robot/khi_rs007n_vac_UNIT1/world_003/base_link_003',
                                      ['link1piv_003', 'link2piv_003', 'link3piv_003', 'link4piv_003',
                                       'link5piv_003', 'link6piv_003'])
       
        asyncio.ensure_future(self.motions[0].startAnimating())
            
        
            


