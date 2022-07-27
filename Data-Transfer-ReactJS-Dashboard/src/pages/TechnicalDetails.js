import './TechnicalDetails.css'
const TechnicalDetails = () => {
    return (
      <div className = "TechnicalDetails">
        <iframe className="uptime" src="http://ec2-35-88-36-61.us-west-2.compute.amazonaws.com:3000/d-solo/vUMFoZrnk/hls-data-transfer-metrics?orgId=1&panelId=16" frameborder="0"></iframe>
        <iframe className="load" src="http://ec2-35-88-36-61.us-west-2.compute.amazonaws.com:3000/d-solo/vUMFoZrnk/hls-data-transfer-metrics?orgId=1&panelId=6" frameborder="0"></iframe>
        
    </div>
    )
  };
  
  export default TechnicalDetails;