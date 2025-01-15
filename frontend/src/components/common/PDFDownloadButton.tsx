import React from 'react';
import { Button, CircularProgress } from '@mui/material';
import { PictureAsPdf } from '@mui/icons-material';
import { jsPDF } from 'jspdf';
import html2canvas from 'html2canvas';

interface PDFDownloadButtonProps {
  content: React.RefObject<HTMLElement>;
  filename?: string;
  label?: string;
  disabled?: boolean;
}

const PDFDownloadButton: React.FC<PDFDownloadButtonProps> = ({
  content,
  filename = 'document.pdf',
  label = 'Download PDF',
  disabled = false,
}) => {
  const [loading, setLoading] = React.useState(false);

  const handleDownload = async () => {
    if (!content.current) return;

    try {
      setLoading(true);
      const canvas = await html2canvas(content.current);
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF({
        orientation: 'portrait',
        unit: 'px',
        format: [canvas.width, canvas.height]
      });

      pdf.addImage(imgData, 'PNG', 0, 0, canvas.width, canvas.height);
      pdf.save(filename);
    } catch (error) {
      console.error('Error generating PDF:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Button
      variant="contained"
      color="primary"
      onClick={handleDownload}
      disabled={disabled || loading}
      startIcon={loading ? <CircularProgress size={20} /> : <PictureAsPdf />}
    >
      {loading ? 'Generating PDF...' : label}
    </Button>
  );
};

export default PDFDownloadButton;
