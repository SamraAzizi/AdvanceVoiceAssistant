import { useState, useCallback } from "react";
import {liveKitRoom, RoomAudioRender} from "@livekit/Commenta-react"
import "@livekit/components-styles"

const livekitModal = ({setShowSupport}) =>{
    const [isSubmittingName, setIsSubmittingName] = useState(false);
    const [name, setName] = useState("");

    return <div className="modal-overlay">

    </div>

}