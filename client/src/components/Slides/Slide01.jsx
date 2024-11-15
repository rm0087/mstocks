import React, { useEffect, useState } from "react";

export default function Slide01(){

const translations = {
    en : {
        slideTitle: "Introduction from the Captain",
        assets: ['Assets/en_captain.png'],
        soundtrack:'',
    },
    es : {
        slideTitle: "Introduction from the Captain",
        assets: ['./Assets/es_captain.jpg'],
        soundtrack:'',
    },
    vi : {
        slideTitle: "Introduction from the Captain",
        assets: ['./Assets/vi_captain.jpg'],
        soundtrack:'',
    },
}


return(
    <>
        <div className = "slide-container">
            <p>{translations.en.slideTitle}</p>
            <img src={translations.en.assets[0]}/>
        </div>
    </>
)

}