import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';

const useStyles = makeStyles({
    root: {
        maxWidth: '400px',
        margin: '15vh 2vw'
    },
    title: {
        fontSize: 16,
    },
    wrap: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        fontSize: 16
    },
});

export default function OrderCard() {
    const classes = useStyles();
    const orderList = [
        {
            id:1,
            date:"下午06:30",
            order: "吉娃娃絲襪奶茶",
            plus:"半糖微冰加大",
            count: 1,
        }
    ]

    return (
        <Card className={classes.root}>
            <CardContent>
                <Typography className={classes.wrap} color="textSecondary" gutterBottom>
                    <span>訂單編號：001</span>
                    <span>
                        {new Intl.DateTimeFormat('zh-TW', {
                            hour: 'numeric',
                            minute: 'numeric',
                        }).format(new Date())}
                    </span>
                </Typography>
                <hr />
                <Grid container spacing={4}>
                    <Grid item xs={6}>
                        吉娃娃絲襪奶茶
                    </Grid>
                    <Grid item xs={4}>
                        半糖少冰 加大
                    </Grid>
                    <Grid item xs={2} text>
                        x 1
                    </Grid>
                </Grid>
            </CardContent>

            <CardActions>
                <Button variant="contained">✖</Button>
                <Button variant="contained" color="secondary">✔</Button>
            </CardActions>
        </Card>
    );
}