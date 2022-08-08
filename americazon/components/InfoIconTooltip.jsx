import React from 'react'
import InfoIcon from '@mui/icons-material/Info';
import Tooltip, { tooltipClasses } from '@mui/material/Tooltip';
import { styled } from '@mui/material/styles';
import Typography from '@mui/material/Typography';

function InfoIconTooltip({ children, iconSize="medium" }) {

  const HtmlTooltip = styled(({ className, ...props }) => (
    <Tooltip {...props} classes={{ popper: className }} />
  ))(({ theme }) => ({
    [`& .${tooltipClasses.tooltip}`]: {
      backgroundColor: '#f5f5f9',
      color: 'rgba(0, 0, 0, 0.87)',
      maxWidth: 265,
      fontSize: theme.typography.pxToRem(12),
      border: '1px solid #006EFF',
      'boxShadow': '10px 10px 5px lightblue'
    },
  }));

  return (
    <HtmlTooltip
      title={
        <React.Fragment>
          <Typography component={"h3"} sx={{ 'font-weight': 'bold' }}>
            {children}
          </Typography>
        </React.Fragment>
      }
      placement='bottom-start'
      enterDelay={25}
      leaveDelay={75}
      fontSize={iconSize}
      arrow
    >
      <InfoIcon className='center'/>
    </HtmlTooltip>
  )
}

export default InfoIconTooltip