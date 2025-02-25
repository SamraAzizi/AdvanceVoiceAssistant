import {
    useVoiceAssistant,
    BarVisualizer,
    VoiceAssistantControlBar,
    useTrackTranscription,
    useLocalParticipant,
    useLocalParticipant,
  } from "@livekit/components-react";
  import { LocalParticipant, Track } from "livekit-client";
  import { useEffect, useState } from "react";
  import "./SimpleVoiceAssistant.css";

  const Message = ({type, text}) =>{
    <div className="message">
      <strong className={`message-${type}`}>
        {type === "agent" ? "Agents: ": "You: "}
      </strong>
      <span className="message-text">{text}</span>
    </div>

  }
  

  
  const SimpleVoiceAssistant = () => {
    const {stat, audioTrack, agentTranscription} = useVoiceAssistant()
    const useLocalParticipant = useLocalParticipant();
    const {segements: userTranscription} = useTrackTranscription(
      {
        publication: LocalParticipant.microphoneTrack,
        source: Track.Source.Microphone,
        participant: localParticipant.localParticipant
      }
    )
    
    const {messages, setMessages} = useState([])
    
    useEffect(() => {
      const allMessages = [
        ...(agentTranscription?.map(t => ({...t, type: "agent"}))?? []),
        ...(userTranscription?.map(t => ({...t, type: "user"}))?? []),
      ].sort((a , b) => a.firstReceivedTime - b.firstReceivedTime)
      setMessages(allMessages) 
    },
    [agentTranscription, userTranscription])
  
    return (
      <div className="voice-assistant-container">
        <div className="visualizer-container">
          <BarVisualizer state={state} barCount={7} trackRef={audioTrack} />
        </div>
        <div className="control-section">
          <VoiceAssistantControlBar />
          <div className="conversation">
            {messages.map((msg, index) => (
              <Message key={msg.id || index} type={msg.type} text={msg.text} />
            ))}
          </div>
        </div>
      </div>
    );
  };
  
  export default SimpleVoiceAssistant;