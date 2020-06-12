import React from 'react';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    menuButton: {
        marginRight: theme.spacing(2),
    },
    title: {
        flexGrow: 1,
    },
}));

export default function BarApp() {
    const classes = useStyles();

    return (
        <div className={classes.root}>
            <AppBar>
                <Toolbar>
                    <img src="../assets/logo.png" alt=""/>
                    <Typography variant="h6" className={classes.title}>
                        吉娃娃美食 後台餐廳
                    </Typography>
                </Toolbar>
            </AppBar>
        </div>
    );
}