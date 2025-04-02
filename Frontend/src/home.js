import React, { useState, useEffect } from "react";
import { makeStyles, withStyles } from "@material-ui/core/styles";
import { AppBar, Toolbar, Typography, Avatar, Container, Card, CardContent, Paper, Grid, Button, CircularProgress, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, CardMedia, CardActionArea, Snackbar } from "@mui/material"; // Update imports here
import { DropzoneArea } from 'material-ui-dropzone';
import logo from "./logo.png";
import image from "./plant.jpeg";
import { Clear } from '@material-ui/icons';
import { common } from '@material-ui/core/colors';
import axios from "axios";
import Alert from '@mui/material/Alert';  // Update import for Alert

const ColorButton = withStyles((theme) => ({
  root: {
    color: theme.palette.getContrastText(common.white),
    backgroundColor: common.white,
    '&:hover': {
      backgroundColor: '#ffffff7a',
    },
  },
}))(Button);

const useStyles = makeStyles((theme) => ({
  grow: { flexGrow: 1 },
  clearButton: {
    width: "100%",
    borderRadius: "15px",
    padding: "15px 22px",
    color: "#000000a6",
    fontSize: "20px",
    fontWeight: 900,
  },
  media: { height: 400 },
  gridContainer: {
    justifyContent: "center",
    padding: "4em 1em 0 1em",
  },
  mainContainer: {
    backgroundImage: `url(${image})`,
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center',
    backgroundSize: 'cover',
    height: "93vh",
    marginTop: "8px",
  },
  imageCard: {
    margin: "auto",
    maxWidth: 400,
    height: 500,
    backgroundColor: 'transparent',
    boxShadow: '0px 9px 70px 0px rgb(0 0 0 / 30%) !important',
    borderRadius: '15px',
  },
  imageCardEmpty: { height: 'auto' },
  tableCell: {
    fontSize: '22px',
    backgroundColor: 'transparent !important',
    borderColor: 'transparent !important',
    color: '#000000a6 !important',
    fontWeight: 'bolder',
    padding: '1px 24px 1px 16px',
  },
  loader: { color: '#be6a77 !important' },
  detail: {
    backgroundColor: 'white',
    display: 'flex',
    justifyContent: 'center',
    flexDirection: 'column',
    alignItems: 'center',
  },
  appbar: {
    background: '#be6a77',
    boxShadow: 'none',
    color: 'white',
  },
  snackbar: {
    position: 'absolute',
    bottom: 20,
    left: '50%',
    transform: 'translateX(-50%)',
  }
}));

export const ImageUpload = () => {
  const classes = useStyles();
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [predictionData, setPredictionData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isImageSelected, setIsImageSelected] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [severity, setSeverity] = useState("info");

  // Handle file selection and preview update
  const handleFileSelection = (files) => {
    if (!files || files.length === 0) {
      resetState();
      return;
    }
    const selectedFile = files[0];
    setFile(selectedFile);
    setIsImageSelected(true);
    setPredictionData(null);  // Reset prediction data when new file is selected
  };

  // Generate preview URL for the selected image
  useEffect(() => {
    if (!file) return;
    const fileUrl = URL.createObjectURL(file);
    setPreview(fileUrl);
  }, [file]);

  // Send the selected file to API for prediction
  const sendFileToAPI = async () => {
    if (!isImageSelected) return;
    const formData = new FormData();
    formData.append("file", file);
    try {
      const response = await axios.post(process.env.REACT_APP_API_URL, formData);
      if (response.status === 200) {
        setPredictionData(response.data);
        setSnackbarMessage("Prediction successful!");
        setSeverity("success");
        setOpenSnackbar(true);
      }
    } catch (error) {
      console.error("Error uploading file: ", error);
      setSnackbarMessage("Failed to process the image.");
      setSeverity("error");
      setOpenSnackbar(true);
    } finally {
      setIsLoading(false);
    }
  };

  // Trigger the API call when preview is available
  useEffect(() => {
    if (!preview) return;
    setIsLoading(true);
    sendFileToAPI();
  }, [preview]);

  // Reset state
  const resetState = () => {
    setFile(null);
    setPreview(null);
    setPredictionData(null);
    setIsImageSelected(false);
  };

  // Clear result data
  const clearPredictionData = () => {
    setPredictionData(null);
    setFile(null);
    setPreview(null);
    setIsImageSelected(false);
  };

  const confidence = predictionData ? (parseFloat(predictionData.confidence) * 100).toFixed(2) : 0;

  return (
    <React.Fragment>
      <AppBar position="static" className={classes.appbar}>
        <Toolbar>
          <Typography variant="h6" noWrap>
            Plant Disease Detection System
          </Typography>
          <div className={classes.grow} />
          <Avatar src={logo} />
        </Toolbar>
      </AppBar>

      <Container maxWidth={false} className={classes.mainContainer} disableGutters>
        <Grid container className={classes.gridContainer} justifyContent="center" alignItems="center" spacing={2}>
          <Grid item xs={12}>
            <Card className={`${classes.imageCard} ${!isImageSelected ? classes.imageCardEmpty : ''}`}>
              {isImageSelected ? (
                <CardActionArea>
                  <CardMedia className={classes.media} image={preview} component="img" title="Uploaded Image" />
                </CardActionArea>
              ) : (
                <CardContent>
                  <DropzoneArea
                    acceptedFiles={['image/*']}
                    dropzoneText="Drag and drop an image of a potato plant leaf to process"
                    onChange={handleFileSelection}
                  />
                </CardContent>
              )}

              {predictionData && (
                <CardContent className={classes.detail}>
                  <TableContainer component={Paper}>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell className={classes.tableCell}>Label:</TableCell>
                          <TableCell align="right" className={classes.tableCell}>Confidence:</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        <TableRow>
                          <TableCell>{predictionData.class}</TableCell>
                          <TableCell align="right">{confidence}%</TableCell>
                        </TableRow>
                      </TableBody>
                    </Table>
                  </TableContainer>
                </CardContent>
              )}

              {isLoading && (
                <CardContent className={classes.detail}>
                  <CircularProgress color="secondary" className={classes.loader} />
                  <Typography variant="h6">Processing...</Typography>
                </CardContent>
              )}
            </Card>
          </Grid>

          {predictionData && (
            <Grid item>
              <ColorButton variant="contained" className={classes.clearButton} onClick={clearPredictionData} startIcon={<Clear fontSize="large" />}>
                Clear
              </ColorButton>
            </Grid>
          )}
        </Grid>
      </Container>

      {/* Snackbar for success/error messages */}
      <Snackbar
        open={openSnackbar}
        autoHideDuration={6000}
        onClose={() => setOpenSnackbar(false)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
        className={classes.snackbar}
      >
        <Alert onClose={() => setOpenSnackbar(false)} severity={severity}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </React.Fragment>
  );
};

export default ImageUpload;
