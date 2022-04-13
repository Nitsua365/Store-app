import { React } from 'react';
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button"
import Grid from '@mui/material/Grid';
import Box from "@mui/material/Box";


function UserLogin() {
  return (
    <div className='Login'>
      <Grid  container direction="column" justifyContent="center" alignItems="center">
        <Grid>
          <Box id="login-box" component="span" sx={{ p: 2, border: '3px light blue'}}>
            <Box sx={{ display: 'inline-grid', gap: 2, gridTemplateRows: 'repeat(3, 1fr)'}}>
              <TextField label="Username" />
              <TextField label="Password" />
            </Box>
          </Box>
        </Grid>
        <Grid>
          <Button variant="outlined" size="large">Login</Button>
        </Grid>
      </Grid>
      
    </div>
  );

}

export default UserLogin;
