function LoadingStatus({theme}){
    return <div className= "loading-container">
        <h2> Generating Your {theme} story </h2>
        <div className="loading-animation">
            <div className="spinner"></div>
        </div>
        <p className="laoding-info">
            Please wait while we generate your story......
        </p>
    </div>
}


export default LoadingStatus;
