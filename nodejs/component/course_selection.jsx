var CourseSelection = React.createClass({
  render: function() {
    return (
      <div id="CourseSelection">
        <div className="ui top attached secondary pointing menu">
          <a className="active item" data-tab="schedule">我的課表</a>
          <a className="item" data-tab="search">Search</a>
        </div>
        <div className="ui bottom attached tab segment active content" data-tab="schedule">

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
      label: {
        times: [
        '08:10-09:00', '09:10-10:00', '10:10-11:00', '11:10-12:00',
        '12:10-13:00', '13:10-14:00', '14:10-15:00', '15:10-16:00',
        '16:10-17:00', '17:10-18:00', '18:30-19:20', '19:30-20:20',
        '20:30-21:20'
        ],
        days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
      },
      rawData:[],
      needRefresh: true
    })
  },
  handleDaysChange: function(event) {
    if ( !event ) return false;
    this.setState({day: event});
  },
  handleLessonsChange: function(event) {
    if ( !event ) return false;
    this.setState({row: event});
  },
  refreshData: function() {
    if (!this.state.needRefresh) return;
    var extendCourse = {}
    this.state.rawData.map(function(element) {
      element.courseTime.map(function(value) {
        extendCourse[Math.floor(value / 100 - 1).toString()] = extendCourse[Math.floor(value / 100 - 1).toString()] || {}
        extendCourse[Math.floor(value / 100 - 1).toString()][(value % 100 - 1).toString()] = element;
      });
    });
    this.setState({extendData: extendCourse});
  },
  componentWillMount: function() {
    this.refreshData();
  },
  componentWillUpdate: function() {
    this.state.needRefresh = !this.state.needRefresh;
    this.refreshData();
  },
  render: function() {
    var daysOption = [5, 6].map(function(currentValue) {
      return (<option key={currentValue} value={currentValue}>{currentValue}</option>)
    }.bind(this));

    var lessonsOption = [10, 11, 12, 13].map(function(currentValue) {
      return (<option key={currentValue} value={currentValue}>{currentValue}</option>)

    }.bind(this));

    /**
     * prepare table
     *
     */
    var thead;
    var tbody;
    var fields;
    /**
     * prepare thead
     * 先產生childern (Days)
     * 利用unshift補上開頭
     */
    fields = this.state.label.days.map(function(currentValue, index) {
      if(index + 1 > this.state.day) return null;
      return (<th key={index + 1} className="two wide center aligned">{currentValue}</th>)
    }.bind(this));
    fields.unshift(<th key={0} className="two wide" />)
    thead = (<thead><tr key={0}>{fields}</tr></thead>);

    /**
     * prepare tbody
     *
     */

    var rows =this.state.label.times.map(function (currentValue, RowIndex) {

      if(RowIndex + 1 > this.state.row) return null;
      /**
       * 這邊好玄喔....Apply的用法，先產生N個元素的空array
       * 接著透過map針對每個element填入資料
       * 參考自 http://stackoverflow.com/questions/1295584/most-efficient-way-to-create-a-zero-filled-javascript-array
       * 最後利用unshift補上時間於row開頭
       */
      fields = Array.apply(null, Array(this.state.day)).map(function(element, index) {
        if(this.state.extendData && this.state.extendData[index.toString()] && this.state.extendData[index.toString()][RowIndex.toString()])
          return (<CourseTableDataField key={index + 1} course={this.state.extendData[index.toString()][RowIndex.toString()]} />)
        return (<CourseTableDataField key={index + 1} />)
      }.bind(this))
      fields.unshift(<td key={0} className="center aligned"><p key={0}>第 {RowIndex + 1} 節</p><p key={1}>{currentValue}</p></td>)
      return (<tr key={RowIndex + 1}>{fields}</tr>)

    }.bind(this))

    tbody = (<tbody>{rows}</tbody>)

    return (
      <div>
        <div className="ui form">
          <div className="two fields">
            <div className="field">
              <select defaultValue={this.state.day} className="ui dropdown daysOption">
                {daysOption}
              </select>
              <label>Days per Week</label>
            </div>
            <div className="field">
              <select defaultValue={this.state.row} className="ui dropdown lessonsOption">
                {lessonsOption}
              </select>
              <label>Lessons per Day</label>
            </div>
          </div>
        </div>

        <table id="CourseTable" className="ui definition table celled">
          {thead}
          {tbody}
        </table>
      </div>
    )
  }
  ,
  componentDidMount: function() {
    $('select.dropdown.daysOption')
      .dropdown({
        onChange: this.handleDaysChange
      })
    ;
    $('select.dropdown.lessonsOption')
      .dropdown({
        onChange: this.handleLessonsChange
      })
    ;
  }
});


/**
 * Data Obj format: (column name)
 * Course Code
 * Course Name
 * Teacher Name
 * Time
 */

var CourseTableDataField = React.createClass({
  render: function() {
    if(this.props.course) {
      return(
        <td>
          <a href="#" onClick={this.props.onClick}><i className="close icon"></i></a>
          <p>{this.props.course.courseName}</p>
        </td>
      );
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
