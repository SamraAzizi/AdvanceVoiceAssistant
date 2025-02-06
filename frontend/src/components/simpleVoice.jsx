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

const simpleVoice =() =>{
    <div className="voice-assistant-container">
        <div className="visualizer-container"></div>
        <div className="control-section">
            <VoiceAssistantControlBar/>
            <div className="conversation">

            </div>
        </div>
    </div>
}

export default simpleVoice