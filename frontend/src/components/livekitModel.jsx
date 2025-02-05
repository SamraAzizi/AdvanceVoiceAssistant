import { useState, useCallback } from "react";
import {liveKitRoom, RoomAudioRender} from "@livekit/Commenta-react"
import "@livekit/components-styles"

const livekitModal = ({setShowSupport}) =>{
    const [isSubmittingName, setIsSubmittingName] = useState(true);
    const [name, setName] = useState("");
    const handleNameSubmit = () =>{};

    return <div className="modal-overlay">
        <div className="modal-content">
            <div className="support-room">
                {isSubmittingName ? (
                    <form onSubmit={handleNameSubmit} className="name-form">
                        <h2>Enter Your Name to Connect With Support</h2>
                        <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Your Name" required/>
                        <button type="submit">Connect</button>
                        <button type="button" className="cancle-button" onClick={() => setShowSupport(false)}>Cancle</button>
                    </form>
                ) : <liveKitRoom
                serverUrl=""
                token=""
                connect={true}
                video={false}
                audio={true}
                onDisconnected={() =>{
                    setShowSupport(false)
                    setIsSubmittingName(true)

                }}

                >
                    <RoomAudioRender></RoomAudioRender>

                </liveKitRoom>
                }

            </div>

        </div>


    </div>

}

export default App