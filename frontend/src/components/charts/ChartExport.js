import React from 'react';

function ChartExport({ chartRef, filename = 'chart' }) {
  const handleExportPNG = () => {
    if (chartRef.current) {
      const url = chartRef.current.toBase64Image();
      const link = document.createElement('a');
      link.download = `${filename}.png`;
      link.href = url;
      link.click();
    }
  };

  const handleExportPDF = async () => {
    // For PDF export, we'll use a simple approach with canvas
    if (chartRef.current) {
      const canvas = chartRef.current.canvas;
      const imgData = canvas.toDataURL('image/png');
      
      // Create a simple PDF using a new window (basic approach)
      // In production, you'd use a library like jsPDF
      const printWindow = window.open('', '', 'height=600,width=800');
      printWindow.document.write('<html><head><title>' + filename + '</title></head><body>');
      printWindow.document.write('<img src="' + imgData + '" style="max-width: 100%;" />');
      printWindow.document.write('</body></html>');
      printWindow.document.close();
      
      // Wait for image to load then print
      setTimeout(() => {
        printWindow.print();
      }, 250);
    }
  };

  return (
    <div className="chart-export-buttons" style={{ marginTop: '10px', display: 'flex', gap: '10px' }}>
      <button onClick={handleExportPNG} className="export-button">
        Export PNG
      </button>
      <button onClick={handleExportPDF} className="export-button">
        Export PDF
      </button>
    </div>
  );
}

export default ChartExport;
