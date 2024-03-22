"""Module for project names definitions"""

from enum import Enum


class ProjectName(str, Enum):
    """Project Names"""

    EPHYS_PLATFORM = "Ephys Platform"
    MSMA_PLATFORM = "MSMA Platform"
    OPHYS_PLATFORM_FP = "Ophys Platform - FP and indicator testing"
    OPHYS_PLATFORM_SLAP2 = "Ophys Platform - SLAP2"
    OPHYS_PLATFORM_HSFP = "Ophys Platform - Multiplexed Neuromodulation"
    BEHAVIOR_PLATFORM = "Behavior Platform"
    MEDULLA = "Medulla"
    THALAMUS = "Thalamus in the middle"
    CELL_TYPE_LUT = "Cell Type LUT"
    DISCOVERY_BWC = "Discovery-Brain Wide Circuit Dynamics"
    DYNAMIC_ROUTING = "Dynamic Routing"
    SCBC = "Single-neuron computations within brain-wide circuits (SCBC)"
    LEARNING_MFISH_V1OMFISH = "Learning mFISH/V1omFISH"
    LEARNING_MFISH = "Learning mFISH"
    V1OMFISH = "V1omFISH"
    OPENSCOPE = "OpenScope"
    BRAIN_COMPUTER_INTERFACE = "Brain Computer Interface"
    COGNITIVE_FLEXIBILITY = "Cognitive flexibility in patch foraging"
    PATCH_FORAGING_POE = "Information seeking in partially observable environments"
    AIND_VIRAL_GENETIC_TOOLS = "AIND Viral Genetic Tools"
    DISCOVERY_NEUROMODULATOR = "Discovery-Neuromodulator circuit dynamics during foraging"
    FORCE_FORAGING = "Force Foraging"
    NEUROBIOLOGY_OF_ACTION = "Neurobiology of Action"
    HIVE = "BRAIN Connects HIVE"
