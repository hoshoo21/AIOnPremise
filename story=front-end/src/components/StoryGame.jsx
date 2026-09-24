import { useState, useEffect } from "react";

function StoryGame({story, onNewStory}){
    const [currentNodeId, setCurrentNodeId] =useState(null);
    const [currentNode, setCurrentNode]= useState(null);
    const [options, setOptions] = useState([]);
    const [isEnding, setIsEnding] = useState(false);
    const [isEndingWinning, setIsEndingWinning] = useState(false);

    useEffect(()=>{
        console.log("story loaded:", story);
        if (story && story.root_node){
            const rootNodeId= story.root_node.id;
            console.log("setting currentNodeId to:", rootNodeId);
            setCurrentNodeId(rootNodeId);
        }
    },[story]);
    
    useEffect(()=>{
        if (currentNodeId && story && story.all_nodes){
            const node = story.all_nodes[currentNodeId];
           
            setCurrentNode(node);
            setIsEnding(node.is_ending);
            setIsEndingWinning(node.is_winning_ending);
            if (!node.is_ending && node.options && node.options.length >0){
                setOptions(node.options);
            }
            else 
            {
                setOptions([]);
            }
        }
    }, [currentNodeId]);
    const chooseOption = (optionId)=>{
        setCurrentNodeId(optionId);
    }
    const restartStory= ()=>{
        if (story && story.root_node){
            setCurrentNodeId(story.root_node.id);
        }
    }
    return <div className="story-game">
        <header className="story-header">
            <h2>{story.title} </h2>

        </header>
        <div className="story-content">
            {currentNode && <div className="story-node">
                <p> {currentNode.content}</p>
                {isEnding ? <div className="story-ending">
                    <h3> {isEndingWinning? "Congratulation": "The End"} </h3>
                        {isEndingWinning? "you have reached winning end": "your adventure has ended"}
                    </div>:
                    <div className="story-otpions"> 
                        <h3> what you will do?</h3>
                        <div className="option-list">
                            {options.map((option,index)=>{
                                return <button key={index} onClick={()=>{chooseOption(option.node_id)}}
                                className="option-btn">
                                    {option.text} 
                                 </button>
                            })}
                        </div>
                    </div>}
             </div>}
             <div className="story-controls">
                <button onClick={restartStory} className="reset-btn"> Restart Story</button>
                {onNewStory && <button onClick={onNewStory} className="new-story-btn" >New Storys</button>}
             </div>
        </div>

    </div>
}

export default StoryGame;