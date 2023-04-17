import React, { useState } from 'react';

interface PopupProps {
  text: string;
}

const Popup: React.FC<PopupProps> = ({ text }) => {
  const [showPopup, setShowPopup] = useState(false);

  return (
    <>
      <div className="popup-button" onClick={() => setShowPopup(true)}>
        ?
      </div>
      {showPopup && (
        <div className="popup-background" onClick={() => setShowPopup(false)}>
          <div className="popup-text" onClick={(e) => e.stopPropagation()}>
            {text}
          </div>
        </div>
      )}
    </>
  );
};

export default Popup;