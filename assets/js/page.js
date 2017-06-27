import React, { Component } from 'react'
import { Link } from 'react-router-dom'

class PageForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            url: ''
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({url: event.target.value});
    }

    handleSubmit(event) {
        event.preventDefault();

        var data = {
            url: this.state.url,
        }

        // Submit form via jQuery/AJAX
        $.ajax({
            type: 'POST',
            url: this.props.url,
            data: data
        })
        .done(function(data) {
            document.location = "#/page/" + data.id;
        })
        .fail(function(jqXhr) {
            console.log('failed to register');
        });
    }

    render() {
        return (
            <div>
                <h1>BlockStamp</h1>
                <p>
                    BlockStamp uses the Bitcoin blockchain to create a permanent record
                    of a web page and gives you a foolproof timestamp to prove it's authenticity.
                </p>
                <form onSubmit={this.handleSubmit}>
                    <div className="row">
                        <div className="large-12 columns">
                            <fieldset>
                                <legend>Enter a URL</legend>
                                <input id="url" name="url" type="url" value={this.state.url} onChange={this.handleChange} required placeholder="http://www.example.com" />
                                <button type="submit" className="large button">Archive and Stamp</button>
                            </fieldset>
                        </div>
                    </div>
                </form>
            </div>
        );
    }
}

class PageDetail extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    loadPageFromServer(id) {
        $.ajax({
            url: 'api/pages/' + id + '/',
            datatype: 'json',
            cache: false,
            success: function(data) {
                this.setState({data: data});
            }.bind(this)
        })
    }

    componentDidMount() {
        this.loadPageFromServer(this.props.match.params.id);
        this.interval = setInterval(() => this.loadPageFromServer(this.props.match.params.id), 10000);
    }


    componentWillUnmount() {
        clearInterval(this.interval);
    }

    render() {
        if (!this.state.data) { return <div /> }
        var page = this.page = this.state.data;
        return (
            <div>
                <h3><a href={page.url} rel="nofollow" target="_blank">{page.title}</a></h3>
                <div className="primary callout">

                    <a className="button" download={`${page.id}.html`} href={`/media/html/${page.id}/${page.id}.html`}>Download Web Page</a>
                    <a className="button" download={`${page.id}.html.ots`} href={`/media/html/${page.id}/${page.id}.html.ots`}>Download Timestamp</a>

                    <p>
                        Status: <strong>{page.status}</strong>
                    </p>
                    { (page.status != "Confirmed") &&
                        <p>
                            Estimated confirmation time: { (page.status == "Pending" ) ? '4 hours': '10 minutes' }
                        </p>
                    }
                    { (page.status == "Waiting") &&
                        <p>
                            Waiting for confirmation of transaction: <code>{ page.tx }</code>
                        </p>
                    }
                    { (page.status == "Pending") &&
                    <p>
                        For instant confirmation, send <code>0.001 BTC</code> to <a href={`bitcoin:${page.address}`}>{page.address}</a>
                    </p>
                    }
                    <p>
                        This timestamp can be verified using <a href="https://opentimestamps.org/" target="_blank">OpenTimestamps</a> after confirmation on the blockchain.
                    </p>
                </div>
                <hr/>
                <iframe id="iframe" sandbox="allow-same-origin allow-scripts allow-popups" src={`/media/html/${page.id}/${page.id}.html`} />
            </div>
        )
    }
}

export { PageDetail, PageForm }
