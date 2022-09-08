import './TransferQueue.css'
const TransferQueue = () => {
    return (
      <div className = "TransferQueue">
        <p className="TransferQueueHeading">Tranfer Queue</p>
        <div className='Transfer1'>
          <p className='Transfer1Value'>Transfer 1</p>
          <div className='eclipse1'>
            <p className='value1'>1</p>
          </div>
          <p className='Transfer1Status'>Ongoing</p>
          <div className='Transfer1Fields'>
            <p className='TotalSize'>Total Size</p>
            <p className='TotalSizeValue'>5 PB</p>
            <p className='DateStarted'>Date Started</p>
            <p className='DateStartedValue'>2 June 2022</p>
            <p className='EstimatedCompletion'>Estimated Completion</p>
            <p className='EstimatedCompletionValue'>2 August 2022</p>
            <div className='viewDataCatalogueButton'>  
              <p className='viewDataCatalogue'>View Data Catalogue</p>
            </div>
          </div>
        </div>
        <div className='Transfer1Line'></div>
        <div className='Transfer2'>
          <p className='Transfer2Value'>Transfer 2</p>
          <div className='eclipse2'>
            <p className='value'>2</p>
          </div>
          <p className='Transfer2Status'>Not Started</p>
          <div className='Transfer2Fields'>
            <p className='TotalSize'>Total Size</p>
            <p className='TotalSizeValue'>5 PB</p>
            <p className='DateStarted'>Date Started</p>
            <p className='DateStartedValue'>-</p>
            <p className='EstimatedCompletion'>Estimated Completion</p>
            <p className='EstimatedCompletionValue'>-</p>
            <div className='viewDataCatalogueButton'>  
              <p className='viewDataCatalogue'>View Data Catalogue</p>
            </div>
          </div>
        </div>
        <div className='Transfer2Line'></div>
        <div className='Transfer3'>
          <p className='Transfer3Value'>Transfer 3</p>
          <div className='eclipse3'>
            <p className='value'>3</p>
          </div>
          <p className='Transfer3Status'>Not Started</p>
          <div className='Transfer3Fields'>
            <p className='TotalSize'>Total Size</p>
            <p className='TotalSizeValue'>5 PB</p>
            <p className='DateStarted'>Date Started</p>
            <p className='DateStartedValue'>-</p>
            <p className='EstimatedCompletion'>Estimated Completion</p>
            <p className='EstimatedCompletionValue'>-</p>
            <div className='viewDataCatalogueButton'>  
              <p className='viewDataCatalogue'>View Data Catalogue</p>
            </div>
          </div>
        </div>
        <div className='Transfer3Line'></div>
      </div>
    )
};
  
export default TransferQueue;
