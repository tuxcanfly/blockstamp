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
                <form onSubmit={this.handleSubmit}>
                    <fieldset id="forms__html5">
                        <legend>New Page</legend>
                        <p>
                            <label htmlFor="url">URL</label>
                            <input id="url" name="url" type="url" value={this.state.url} onChange={this.handleChange} placeholder="http://www.example.com" size="80" />
                        </p>
                        <p><button type="submit">Stamp</button></p>
                    </fieldset>
                </form>
            </div>
        );
    }
}

class PageList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    loadPagesFromServer() {
        $.ajax({
            url: this.props.url,
            datatype: 'json',
            cache: false,
            success: function(data) {
                this.setState({data: data});
            }.bind(this)
        })
    }

    componentDidMount() {
        this.loadPagesFromServer();
    }

    render() {
        var pageNodes = []
        if (this.state.data) {
            pageNodes = this.state.data.map(function(page){
                return (
                    <li key={page.id}>
                        <Link to={`page/${page.id}`}>{page.title}</Link>
                    </li>
                )
            })
        }
        return (
            <div>
                <h1>BlockStamp</h1>
                <p>
                    BlockStamp timestamps a url archive using the blockchain.
                </p>
                <PageForm url="api/pages/" />
                {pageNodes.length > 0 &&
                <div>
                    <h1>Recently confirmed</h1>
                    <ul>
                        {pageNodes}
                    </ul>
                </div>
                }
            </div>
        )
    }
}

class PageDetail extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    loadPageFromServer() {
        $.ajax({
            url: 'api/pages/' + this.props.match.params.id + '/',
            datatype: 'json',
            cache: false,
            success: function(data) {
                this.setState({data: data});
            }.bind(this)
        })
    }

    componentDidMount() {
        this.loadPageFromServer();
    }

    render() {
        if (!this.state.data) { return <div /> }
        var page = this.page = this.state.data;
        return (
            <div>
                <h1>BlockStamp</h1>
                <h3><a href={page.url} rel="nofollow" target="_blank">{page.title}</a></h3>
                <fieldset>
                <p>
                    <label>Status: <bold>{page.status}</bold></label>
                    <ul>
                        <li>
                            <a download={`${page.id}.html`} href={`/media/html/${page.id}/${page.id}.html`}>Download Web Page</a>
                        </li>
                        <li>
                            <a download={`${page.id}.html.ots`} href={`/media/html/${page.id}/${page.id}.html.ots`}>Download Timestamp</a>
                        </li>
                    </ul>
                </p>
                </fieldset>
                <p>
                    This timestamp can be verified using <a href="https://opentimestamps.org/" target="_blank">OpenTimestamps</a> after confirmation on the blockchain.
                </p>
                <p>
                    Estimated confirmation time: 4 hours
                </p>
                <p>
                    For instant confirmation, send 0.005 BTC to <a href={`bitcoin:${page.address}`}>{page.address}</a>
                </p>
                <hr/>
                <iframe id="iframe" src={`/media/html/${page.id}/${page.id}.html`} />
            </div>
        )
    }
}

export { PageList, PageDetail, PageForm }
