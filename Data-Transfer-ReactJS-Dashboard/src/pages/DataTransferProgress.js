
import './DataTransferProgress.css';

const DataTransferProgress = () => {

  return (
  <div className = "DataTransferProgress">
    <iframe className='clock' src="http://ec2-35-88-36-61.us-west-2.compute.amazonaws.com:3000/d-solo/vUMFoZrnk/hls-data-transfer-metrics?orgId=1&refresh=5s&panelId=20" frameborder="0"></iframe>
    <iframe className='sealedstate' src="http://ec2-35-88-36-61.us-west-2.compute.amazonaws.com:3000/d-solo/vUMFoZrnk/hls-data-transfer-metrics?orgId=1&refresh=5s&panelId=4" frameborder="0"></iframe>
    <iframe className='piechart' src="http://ec2-35-88-36-61.us-west-2.compute.amazonaws.com:3000/d-solo/vUMFoZrnk/hls-data-transfer-metrics?orgId=1&refresh=5s&panelId=2" frameborder="0"></iframe>

    <iframe className='transferspeed' src="http://ec2-35-88-36-61.us-west-2.compute.amazonaws.com:3000/d-solo/vUMFoZrnk/hls-data-transfer-metrics?orgId=1&refresh=5s&panelId=22" frameborder="0"></iframe>
    <iframe className='timetocompletetransfer' src="http://ec2-35-88-36-61.us-west-2.compute.amazonaws.com:3000/d-solo/vUMFoZrnk/hls-data-transfer-metrics?orgId=1&refresh=5s&panelId=28" frameborder="0"></iframe>
    <iframe className='totaldatatransferred' src="http://ec2-35-88-36-61.us-west-2.compute.amazonaws.com:3000/d-solo/vUMFoZrnk/hls-data-transfer-metrics?orgId=1&refresh=5s&panelId=26" frameborder="0"></iframe>
    <iframe className='totalestimatedcost' src="http://ec2-35-88-36-61.us-west-2.compute.amazonaws.com:3000/d-solo/vUMFoZrnk/hls-data-transfer-metrics?orgId=1&refresh=5s&panelId=30" frameborder="0"></iframe>

  </div>
  )
  };
  
  export default DataTransferProgress;