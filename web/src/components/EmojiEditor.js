import React from 'react'
import {makeStyles} from '@material-ui/core/styles';
import Grid from "@material-ui/core/Grid";
import Intensifies from "./editors/Intensifies";
import Original from "./editors/Original";
import Party from "./editors/Party";

const useStyles = makeStyles({
    root: {
        flexGrow: 1,
    },
});

export default function EmojiEditor({match}) {
    const classes = useStyles();

    return (
        <div className={classes.root}>
            <Grid
                container
                direction="row"
                justify="center"
                spacing={2}
            >
                <Original id={match.params.id}/>
                <Intensifies id={match.params.id}/>
                <Party id={match.params.id}/>
            </Grid>
        </div>
    )
}