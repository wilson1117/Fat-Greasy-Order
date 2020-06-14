import React, { useState, useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Snackbar from '@material-ui/core/Snackbar';

const useStyles = makeStyles({
    root: {
        minWidth: '400px',
        height: 'auto',
        margin: '2vh 3% 0 3%',
        display: 'flex',
        justifyContent: 'center',
        flexDirection: 'column',
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
    const [orderList, setOrderList] = useState([]);
    useEffect(() => {
       let refresh = setInterval(getOrder, 1000);
    }, [])

    const getOrder = () => {
        const apiURL = 'http://localhost:8000/';
        fetch(apiURL)
            .then(res => res.json())
            .then(data => {
                setOrderList(data);
                console.log("更新")

            })
            .catch((err) => {
                console.log(err)
            })
    }

    const delOrder = (index) => {
        const apiURL = 'http://localhost:8000/del_order?_id='+index;
        fetch(apiURL,{mode:'no-cors'})
            .then(res => res.json())
            .then(data => {
                console.log(data)

            })
            .catch((err) => {
                console.log(err)
            })

    }


    return (
        <Grid container>
            {orderList.map((item, index) =>
                <Card className={classes.root}>
                    <CardContent>
                        <Typography className={classes.wrap} color="textSecondary" gutterBottom>
                            <span>訂單編號：{`00${index + 1}`}</span>
                            <span>{'外帶'}</span>
                        </Typography>
                        <hr />
                        {item.food.map(food =>
                            <Grid container spacing={2}>
                                <Grid item xs={5}>
                                    {food.name}
                                </Grid>
                                <Grid item xs={5}>
                                    {food.plus?.ice ? food.plus.ice + ',' : ''}
                                    {food.plus?.sugar ? food.plus.sugar + ',' : ''}
                                    {food.plus?.size ? food.plus?.size : ''}
                                </Grid>
                                <Grid item xs={2} text>
                                    {'x' + food.count}
                                </Grid>
                            </Grid>

                        )}
                    </CardContent>

                    <CardActions style={{ marginLeft: '75%' }}>
                        <Button variant="contained" color="secondary" onClick={() => { delOrder(item._id) }}>✔</Button>
                    </CardActions>
                </Card>)}
        </Grid>

    );
}