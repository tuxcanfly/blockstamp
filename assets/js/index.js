var React = require('react')
var ReactDOM = require('react-dom')

class PageForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            url: ''
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    clearForm() {
        document.getElementById("url").clear();
    }

    handleChange(event) {
        this.setState({url: event.target.value});
    }

    handleSubmit(event) {
        event.preventDefault();

        console.log(this.state);

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
            this.clearForm()
        })
        .fail(function(jqXhr) {
            console.log('failed to register');
        });
    }

    render() {
        return (
            <div>
                <h1>New Stamp</h1>
                <form onSubmit={this.handleSubmit}>
                    <label htmlFor="url">
                        URL:
                    </label>
                    <input id="url" name="url" type="text" value={this.state.url} onChange={this.handleChange} />
                    <input type="submit" value="Submit" />
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

    loadPagesFromServer(){
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
            console.log('DATA!')
            var pageNodes = this.state.data.map(function(page){
                return <li key={page.id}> {page.title} </li>
            })
        }
        return (
            <div>
                <h1>Recent stamps</h1>
                <ul>
                    {pageNodes}
                </ul>
            </div>
        )
    }
}

ReactDOM.render(<PageList url='/api/pages/' />, document.getElementById('container'))
ReactDOM.render(<PageForm url='/api/pages/' />, document.getElementById('form'));
