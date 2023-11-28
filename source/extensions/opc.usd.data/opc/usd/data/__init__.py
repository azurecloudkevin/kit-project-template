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
from .extension import *
omni.kit.pipapi.install("python-dotenv", module="dotenv")
omni.kit.pipapi.install("os")
omni.kit.pipapi.install("sys")
omni.kit.pipapi.install("time")
omni.kit.pipapi.install("pxr")
import os

from dotenv import dotenv_values, find_dotenv, load_dotenv

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), f"..{os.sep}..{os.sep}..{os.sep}..{os.sep}..{os.sep}pip-packages"))
dotenv_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), f"..{os.sep}..{os.sep}..{os.sep}..{os.sep}.env")
load_dotenv(dotenv_path)