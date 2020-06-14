import React from 'react';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
    title: {
        flexGrow: 1,
        color: '#000'
    },
    bgcolor: {
        background: '#81d4fa',

    }
}));

export default function BarApp() {
    const classes = useStyles();

    return (
        <AppBar position="static">
            <Toolbar className={classes.bgcolor}>
                <img src={require('../assets/logo.png')} alt="" style={{ width: '5%', height: '5%' }} />
                <Typography variant="h6" className={classes.title}>
                    ～肥宅油膩指定～後台訂單
                </Typography>
            </Toolbar>
        </AppBar>
    );
}