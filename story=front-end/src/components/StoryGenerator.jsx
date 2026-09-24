// @ts-nocheck
import { useState,useEffect } from "react";

import { useNavigate} from "react-router-dom";

import axios from "axios";

import ThemeInput from "./ThemeInput";

import LoadingStatus from "./loadingStatus";

const API_BASE_URL='http://localhost:8000/api';

function StoryGenerator(){
    const navigate = useNavigate();
    const [theme,setTheme]= useState("");
    const [jobId, setJobId] = useState(null);
    const [jobStatus, setJobStatus] = useState(null);
    const [error, setError] = useState(null);
    const [loading,setLoading] = useState(false);


    useEffect(()=>{
        let poolInerval;
        if(jobId && jobStatus ==="processing"){
            poolInerval= setInterval(()=>{
                pollJobStatus(jobId)
            },5000);
        
        }
        return()=>{
            if (poolInerval){
                clearInterval(poolInerval);
            }
        }

    },[jobId,jobStatus])
    const reset = ()=>{
        setJobId(null);
        setJobStatus(null);
        setError(null);
        setTheme("");
        setLoading(false);
    }
    
    const gneerateStory = async(theme)=>{
        setLoading(true);
        setError(null);
        setTheme(theme);
        try{
            const response = await axios.post(`${API_BASE_URL}/stories/create`, {theme});
            const {job_id, status} =response.data; 
            setJobId(job_id);
            pollJobStatus(job_id);
        }
        catch(err){
            setLoading(false);
            setError("Failed to generate story");
        }
    }   
    const pollJobStatus = async(id)=>{
        try{
            const response =  await axios.get(`${API_BASE_URL}/jobs/${id}`);

            const {status,session_id, job_error}=response.data;
            setJobStatus(status);
            if (status==="completed" && session_id){
                fetchStory(session_id);
            }
            else if (status==="failed" ||job_error){
                setError("Failed to generate Story");
                setLoading(false);
            }
        }
        catch(err){
            if (err.response?.status!==404){
                setError(`failed to fetch story status :${err.message}`);
                setLoading(false);
            }
        }
    }
    const fetchStory = async (id) => {
        try {
            setLoading(false)
            setJobStatus("completed")
            navigate(`/story/${id}`)
        } catch (e) {
            setError(`Failed to load story: ${e.message}`)
            setLoading(false)
        }
    }
    
    return <div className="story-generator">
        {error && <div className="error-message">
            <p>{error}</p>
            <button onClick = {reset}>Try Again </button>
            </div>}
        {!jobId && !error && !loading && <ThemeInput onSubmit={gneerateStory}/>}
        {loading && <LoadingStatus theme={theme}/>}
    </div>
}

export default StoryGenerator;