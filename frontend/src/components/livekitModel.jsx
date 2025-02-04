import { useState, useCallback } from "react";
import {liveKitRoom, RoomAudioRender} from "@livekit/Commenta-react"
import "@livekit/components-styles"

const livekitModal = ({setShowSupport}) =>{
    const [isSubmittingName, setIsSubmittingName] = useState(false);
    const [name, setName] = useState("");
    const handleNameSubmit = () =>{};

    return <div className="modal-overlay">
        <div className="model-content">
            <div className="support-room">
                {isSubmittingName ? (
                    <form onSubmit={handleNameSubmit} className="name-form">
                        <h2>Enter Your Name to Connect With Support</h2>
                        <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Your Name" required/>
                    </form>
                ) : <></>}

            </div>

        </div>

    </div>

}