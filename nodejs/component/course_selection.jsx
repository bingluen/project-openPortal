var CourseSelection = React.createClass({
  render: function() {
    return (
      <div id="CourseSelection">
        <div className="ui top attached secondary pointing menu">
          <a className="active item" data-tab="schedule">我的課表</a>
          <a className="item" data-tab="search">Search</a>
        </div>
        <div className="ui bottom attached tab segment active" data-tab="schedule">
          <CourseTable />
        </div>
        <div className="ui bottom attached tab segment" data-tab="search">
          <p>搜尋課表</p>
          <p></p>
        </div>
      </div>
    )
  }
});

var CourseTable = React.createClass({
  getInitialState: function () {
    return({
      day: 6,
      row: 13,
      lable: {
        times: [
        '08:10-09:00', '09:10-10:00', '10:10-11:00', '11:10-12:00',
        '12:10-13:00', '13:10-14:00', '14:10-15:00', '15:10-16:00',
        '16:10-17:00', '17:10-18:00', '18:30-19:20', '19:30-20:20',
        '20:30-21:20'
        ],
        days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
      },
      data: [['test']]
    })
  },
  render: function() {
    return(
      <table id="CourseTable" className="ui very basic collapsing definition celled table">
        <CourseTableHead day={this.state.day} lable={this.state.lable.days} />
        <CourseTableBody day={this.state.day} row={this.state.row} lable={this.state.lable.times} data={this.state.data} />
      </table>
    )
  }
});

var CourseTableHead = React.createClass({
  render: function() {
    var heads = this.props.lable.slice(0, this.props.day).map(function(currentValue, index) {
      return (<th>{currentValue}</th>);
    });
    heads.unshift(<th/>)
    return(
      <thead>
        <tr>
          {heads}
        </tr>
      </thead>
    )
  }
})

var CourseTableBody = React.createClass({
  handleChildClick: function(childData, events) {
    console.log(childData);
    console.log(events);
  },
  render: function() {
    var rows = this.props.lable.slice(0, this.props.row).map(function(currentValue, index) {
      if(this.props.data && this.props.data.length > index && this.props.data[index])
      {
        return (<CourseTableRow day={this.props.day} time={currentValue} data={this.props.data[index]} />)
      } else {
        return (<CourseTableRow day={this.props.day} time={currentValue} data={''}/>)
      }
    }.bind(this))

    return (
      <tbody>
        {rows}
      </tbody>
    )
  }
})

var CourseTableRow = React.createClass({
  render: function() {
    var columns = []
    for(var index = 0; index < this.props.day ; index++)
    {
      if(this.props.data[index])
        columns.push (
          <CourseTableDataField data={this.props.data[index]} />
        )
      else
        columns.push (
          <CourseTableDataField />
        )

    }

    return (
      <tr>
        <td>{this.props.time}</td>
        {columns}
      </tr>
      )
  }
})

var CourseTableDataField = React.createClass({
  render: function()
  {
    if(this.props.data) {
      return( <td><a href="#" onClick={this.props.onClick}> {this.props.data}</a></td> );
    } else {
      return( <td></td>)
    }
  }
});



$(document).ready(function() {
  $('.menu .item')
    .tab()
  ;
});
