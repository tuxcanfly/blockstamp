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
        if (this.state.data) {
            var pageNodes = this.state.data.map(function(page){
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
                <h1>Recently confirmed</h1>
                <ul>
                    {pageNodes}
                </ul>
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

    save(data, filename) {
        if(!data) {
            return;
        }

        if(!filename) filename = ''

        if(typeof data === "object"){
            data = JSON.stringify(data, undefined, 4)
        }

        var blob = new Blob([data], {type: 'text/html'}),
            e    = document.createEvent('MouseEvents'),
            a    = document.createElement('a')

        a.download = filename
        a.href = window.URL.createObjectURL(blob)
        a.dataset.downloadurl =  ['text/html', a.download, a.href].join(':')
        e.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null)
        a.dispatchEvent(e)
    }

    render() {
        if (!this.state.data) { return <div /> }
        var page = this.state.data;
        return (
            <div>
                <h1>BlockStamp</h1>
                <h3><a href={page.url} rel="nofollow" target="_blank">{page.title}</a></h3>
                <fieldset>
                <p>
                    <label>Status: <bold>{page.status}</bold></label>
                    <button type="button" onClick={  ()=> { this.save(page.body, page.id+".html") } }>Download File</button>
                    <a download={`${page.id}.html.ots`} href={`data:application/octet-stream;base64,${page.signature}`}>Download Timestamp</a>
                </p>
                </fieldset>
                <p>This timestamp can be verified using <a href="https://opentimestamps.org/" target="_blank">OpenTimestamps</a> after confirmation on the blockchain.</p>
                <hr/>
                <iframe id="iframe" srcDoc={page.body} />
            </div>
        )
    }
}

export { PageList, PageDetail, PageForm }
