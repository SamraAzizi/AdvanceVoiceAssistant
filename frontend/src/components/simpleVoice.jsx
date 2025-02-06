import { Component } from "react";
import{
    useVoiceAssistant,
    BarVisualizer,
    VoiceAssistantControllBar,
    useTrackTranscripant,
    useLocalPaticipant
}
from "@livekit/Components-react"
import { Track } from "livekit-client";
import { useEffect, useState } from "react";
import "./simpleVoice.css"