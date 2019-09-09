import React from 'react';
import {makeStyles} from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardMedia from "@material-ui/core/CardMedia";
import {Typography} from "@material-ui/core";
import CardContent from "@material-ui/core/CardContent";
import Button from "@material-ui/core/Button";
import CardActions from "@material-ui/core/CardActions";
import Grid from "@material-ui/core/Grid";
import CircularProgress from "@material-ui/core/CircularProgress";


const useStyles = makeStyles(theme => ({
    card: {
        maxWidth: 500,
    },
    media: {
        height: 128,
        width: 128,
        margin: 'auto',
        objectFit: 'contain'
    },
    margin: {
        height: theme.spacing(3),
    },
    loading: {
        margin: '-128px auto 0 auto',
        display: 'block',
        textAlign: 'center'
    },
    loadingImg: {
        opacity: 0.2
    }
}));

export default function EditorCard(props) {

    const classes = useStyles();

    const imgClass = props.loading ? classes.media + ' ' + classes.loadingImg : classes.media;

    return (
        <Grid item xs>
            <Card className={classes.card}>
                <CardMedia
                    component="img"
                    height="128"
                    image={props.url}
                    className={imgClass}/>
                {props.loading && <div className={classes.loading}>
                    <CircularProgress className={classes.progress} size={128} thickness={2} />
                </div>}
                <CardContent>
                    <Typography gutterBottom variant="h5" component="h2">:{props.name}:</Typography>
                    {props.controls}
                </CardContent>
                <CardActions>
                    <Button size="small" color="primary" href={props.url + '?download'}>Download</Button>
                </CardActions>
            </Card>
        </Grid>
    )
}