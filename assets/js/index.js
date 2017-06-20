var React = require('react')
var ReactDOM = require('react-dom')

var PageList = React.createClass({
    loadPagesFromServer: function(){
        $.ajax({
            url: this.props.url,
            datatype: 'json',
            cache: false,
            success: function(data) {
                this.setState({data: data});
            }.bind(this)
        })
    },

    getInitialState: function() {
        return {data: []};
    },

    componentDidMount: function() {
        this.loadPagesFromServer();
        setInterval(this.loadPagesFromServer, 
                    this.props.pollInterval)
    }, 
    render: function() {
        if (this.state.data) {
            console.log('DATA!')
            var pageNodes = this.state.data.map(function(page){
                return <li> {page.title} </li>
            })
        }
        return (
            <div>
                <h1>Hello World!</h1>
                <ul>
                    {pageNodes}
                </ul>
            </div>
        )
    }
})

ReactDOM.render(<PageList url='/api/pages/' pollInterval={1000} />, document.getElementById('container'))
