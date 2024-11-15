import React, { useState, useRef } from "react";
import slideContent from "./slide-content.json";
const { slides } = slideContent;

export default function App() {
    const [currentIndex, setCurrentIndex] = useState(0);
    const [slideType, setSlideType] = useState(slides[currentIndex].type);
    const [language, setLanguage] = useState("en")
    const [isPlaying, setIsPlaying] = useState(true)
    const audioRef = useRef(null);
    const videoRef = useRef(null);

    // SLIDE TEMPLATES //////////////////////////////////////////////////////////////////////////
    const TitleSlide = ({ content }) => (
        <div>
            <h1>{content[language].title}</h1>
        </div>
    );

    const TextOnlySlide = ({ content }) => (
        <div>
            <p>{content[language].text}</p>
        </div>
    );

    const TextAndMediaSlide = ({ content }) => {
        
        //if listpoints is not empty, map list points
        const listPoints = content[language].listPoints?.map((point) =>
            point ? <li>{point}</li> : null
        )
        
        // if content.images is not empty, map images
        const medias = content.images?.map((media) =>
            media? <img src={media} alt="Slide Media" /> : null    
        )

        return (
            <div>
                <div id = "title">
                    <h1>{content[language].title}</h1>
                </div>
                <div id = "slide-content">
                    <h3>{content[language].listHeads?.[0] || ""}</h3>
                    {listPoints}
                    <div id = "medias">
                        {medias}
                    </div>
                </div>
            
            </div>
        )
    };

    const TextAndMediaSlideRight = ({ content }) => {
        
        //if listpoints is not empty, map list points
        const listPoints = content[language].listPoints?.map((point) =>
            point ? <li>{point}</li> : null
        )
        
        // if content.images is not empty, map images
        const medias = content.images?.map((media) =>
            media? <img src={media} alt="Slide Media" /> : null    
        )

        return (
        <div>
            <div id = "title">
                <h1>{content[language].title}</h1>
            </div>
            <div id = "slide-content-right">
                <h3>{content[language].listHeads?.[0] || ""}</h3>
                {listPoints}
                <div id = "medias-right">
                    {medias}
                </div>
            </div>
            
        </div>
        )
    };

    const MediaOnlySlide = ({ content }) => (
        <div>
            {/* <img src={content[language].imageUrl} alt="Slide Media" /> */}
            <h1>{content[language].title}</h1>
        </div>
    );

    const QuizSlide = ({ content }) => (
        <div>
            <h1>{content[language].question}</h1>
            <ul>
                {content[language].options.map((option, index) => (
                    <li key={index}>{option}</li>
                ))}
            </ul>
        </div>
    );

    const MediaAndQuizSlide = ({ content }) => (
        <div>
            <img src={content[language].imageUrl} alt="Slide Media" />
            <h1>{content[language].question}</h1>
            <ul>
                {content[language].options.map((option, index) => (
                    <li key={index}>{option}</li>
                ))}
            </ul>
        </div>
    );
    // END SLIDE TEMPLATES //////////////////////////////////////////////////////////////////////
    
    const goToNextSlide = () => {
        const newIndex = (currentIndex + 1) % slides.length;
        const newSlideType = slides[newIndex].type;
        setCurrentIndex(newIndex);
        setSlideType(newSlideType);
    };

    const goToPreviousSlide = () => {
        const newIndex = (currentIndex - 1 + slides.length) % slides.length;
        const newSlideType = slides[newIndex].type;
        setCurrentIndex(newIndex);
        setSlideType(newSlideType);
    };

    const toggleMediaPlayback = () => {
        if (isPlaying) {
          audioRef.current?.pause();
          videoRef.current?.pause();
        } else {
          audioRef.current?.play();
          videoRef.current?.play();
        }
        setIsPlaying(!isPlaying);
      };

    // Define slide templates based on slideType
    const renderSlide = () => {
        switch (slideType) {
            case "0":
                return <TitleSlide content={slides[currentIndex]} />;
            case "1":
                return <TextOnlySlide content={slides[currentIndex]} />;
            case "2":
                return <TextAndMediaSlide content={slides[currentIndex]} />;
            case "3":
                return <MediaOnlySlide content={slides[currentIndex]} />;
            case "4":
                return <QuizSlide content={slides[currentIndex]} />;
            case "5":
                return <MediaAndQuizSlide content={slides[currentIndex]} />;
            case "6":
                return <TextAndMediaSlideRight content={slides[currentIndex]} />;
            default:
                return <div>Unknown slide type</div>;
        }
    };
<<<<<<< HEAD
<<<<<<< HEAD
    useEffect(() => {
        const fetchCompanyJsonTest = async () => {
            setSearchValue('');
        
            try {
                const response = await fetch(`/companyfacts2/${company.ticker}`);
                if (!response.ok) {
                    throw new Error('Failed to find company');
                }
        
                const data = await response.json();
                console.log(data);
            } catch (error) {
                console.error('Error searching companies:', error);
            }
        };
        // fetchCompanyJsonTest()
    }, [company.ticker]);
   
        // <Router>
        //     <Navbar />
            
        //     <Switch>
        //         <Route path="/financials" render={() => <Financials apiInfo={apiInfo}/>} />
        //         <Route path="/keywords" render={() => <Keywords company={company} />} />
        //         {/* <Route path="/comments" render={() => <Note company={company} />} />
        //         <Route path="/map" render={() => <Map company={company} />} /> */}
        //     </Switch>
        // </Router>
    return(
=======

    const handleLanguage = (key) => setLanguage(key)
    return (
>>>>>>> 027a1bb4c4a126cec720bcdaa857a13202c55d1c
=======

    const handleLanguage = (key) => setLanguage(key)
    return (
>>>>>>> 027a1bb4c4a126cec720bcdaa857a13202c55d1c
        <>
            {slideContent[language] && slideContent[language].soundtrack && <audio ref={audioRef} src={slideContent[language].soundtrack} loop />}
            {Object.entries(slideContent.languages).map(([key,language]) =>
                <button key={key} onClick={()=>handleLanguage(key)}>{language}</button>
            )}
            <div id = "slideshow-container">
                <div>{renderSlide()}</div>
            </div>
            <div id = "control-panel">
                <div id = "controls">
                    <button onClick={goToPreviousSlide}>Previous</button>
                    <button onClick={toggleMediaPlayback}>
                        {isPlaying ? 'Pause' : 'Play'}
                    </button>
                    <button onClick={goToNextSlide}>Next</button>
                </div>
                <div id = "test-stats">
                    <p>currentIndex: {currentIndex}</p>
                    <p>Slide ID: {slides[currentIndex].id}</p>
                    <p>slideType: {slideType} - {slideContent.slideTypes[slideType]}</p>
                    <p>language: {language}</p>
                    
                </div>
            </div>
        </>
    );
}
