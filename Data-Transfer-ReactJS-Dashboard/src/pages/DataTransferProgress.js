
import './DataTransferProgress.css';
import configData from '../config.json';

const DataTransferProgress = () => {

  return (
  <div className = "DataTransferProgress">
    <iframe className='clock' src={configData.DATA_TRANSFER_PROGRESS.CLOCK} frameborder="0"></iframe>
    <iframe className='sealedstate' src={configData.DATA_TRANSFER_PROGRESS.SEALED_STATE} frameborder="0"></iframe>
    <iframe className='piechart' src={configData.DATA_TRANSFER_PROGRESS.PIE_CHART} frameborder="0"></iframe>
    <iframe className='transferspeed' src={configData.DATA_TRANSFER_PROGRESS.TRANSFER_SPEED} frameborder="0"></iframe>
    <iframe className='timetocompletetransfer' src={configData.DATA_TRANSFER_PROGRESS.TIME_TO_COMPLETE_TRANSFER} frameborder="0"></iframe>
    <iframe className='totaldatatransferred' src={configData.DATA_TRANSFER_PROGRESS.TOTAL_DATA_TRANSFERRED} frameborder="0"></iframe>
    <iframe className='totalestimatedcost' src={configData.DATA_TRANSFER_PROGRESS.TOTAL_ESTIMATED_COST} frameborder="0"></iframe>
  </div>
  )
};
 
export default DataTransferProgress;
