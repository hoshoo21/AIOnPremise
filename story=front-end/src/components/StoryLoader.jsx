import { useState , useEffect} from "react";
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import LoadingStatus from "./loadingStatus";
import StoryGame from "./StoryGame";

const API_BASE_URL='http://localhost:8000/api';

function StoryLoader(){

    const {id} = useParams();
    const navigate = useNavigate();
    const [story, setStory]= useState(null);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState(null);
    
    const loadStory=async(storyId)=>{
        setLoading(true);
        setError(null);
        try{
            console.log(`${API_BASE_URL}/stories/${storyId}/complete`);
            const response = await axios.get(`${API_BASE_URL}/stories/${storyId}/complete`);
            console.log(response.data);
            setStory(response.data);
            setLoading(false);

        }
        catch(error){
            if (error.response?.status ===404){
                setError("Story Not found");
            }
            else {
                setError("Failed to load story")
            }
        }
        finally{
            setLoading(false);
        }
    }
    useEffect(()=>{
        loadStory(id);
    },
    [id])
    const createNewStory=()=>{
        navigate("/");
    }
    if (loading){
        return <LoadingStatus theme="story"/>
    
    }
    if (error){
        return <div className='error-message'>
            <h2>Story Not found</h2>
            <p>{error}</p>
            <button onClick={createNewStory}>Goto story Genertor</button>
        </div>
        

    }
    if (story){
        return <div className="story=loader">
            <StoryGame story={story} onNewStory={createNewStory} />
        </div>
    }


}

export default StoryLoader;

