var CourseSelection = React.createClass({
  getInitialState: function() {
    return(
      {
        list: []
      }
    )
  },
  handleAddCourse: function(course) {
    var list = this.state.list;
    list.push(course);
    this.setState({list: list})
  },
  render: function() {
    return (
      <div id="CourseSelection">
        <div className="ui top attached secondary pointing menu">
          <a className="active item" data-tab="schedule">我的課表</a>
          <a className="item" data-tab="search">Search</a>
        </div>
        <div className="ui bottom attached tab segment active content" data-tab="schedule">

          <CourseTable courseList={this.state.list} />
        </div>
        <div className="ui bottom attached tab segment" data-tab="search">

          <SearchCourse handleAddCourse={this.handleAddCourse}/>
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
  refreshData: function(courseList) {
    var extendCourse = {}
    courseList.map(function(element) {
      element.courseTime.map(function(value) {
        /* 若課表天數不夠，自動增加 */
        if( Math.floor(value / 100) > this.state.day ) {
          $('.dropdown.daysOption')
            .dropdown('set selected', Math.floor(value / 100))
          ;
        }
        /* 若課表節數不夠，自動增加 */
        if( value % 100 > this.state.row) {
          $('.dropdown.lessonsOption')
            .dropdown('set selected', value % 100)
          ;
        }
        extendCourse[Math.floor(value / 100 - 1).toString()] = extendCourse[Math.floor(value / 100 - 1).toString()] || {}
        extendCourse[Math.floor(value / 100 - 1).toString()][(value % 100 - 1).toString()] = element;
      }.bind(this));
    }.bind(this));
    this.setState({extendData: extendCourse});
  },
  componentWillReceiveProps: function() {
    this.refreshData(this.props.courseList);
  },
  render: function() {
    console.log()
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
  },
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
 * course uid
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
          <a href="#" className="right floated"><i className="close icon"></i></a>
          <p className="center aligned">{this.props.course.courseName}<br/>{this.props.course.teacherName}</p>
        </td>
      );
    } else {
      return( <td></td>)
    }
  }
});

var SearchCourse = React.createClass({
  getInitialState: function() {
    $.ajax({
      url: 'course_database.json',
      type: 'get',
      dataType: 'json'

    })
    .done(function(data, textStatus, jqXHR) {
      this.setState({courseData: data});
    }.bind(this))
    .fail(function(jqXHR, textStatus, errorThrown) {
    });

    return ( {
      degree: [1, 2, 3, 4],
      reslut: {}
    } )
  },
  handleSearchFormSubmit: function(keys) {

    var result = this.state.courseData.course;

    if(keys.department) {
      result = result.filter(function(element, index, array) {
        return element.department == keys.department;
      });
    }

    if(keys.degree) {
      result = result.filter(function(element, index, array) {
        return element.degree == keys.degree;
      });
    }

    if(keys.courseCode) {
      result = result.filter(function(element, index, array) {
        return element.code.indexOf(keys.courseCode) >= 0;
      });
    }

    if(keys.courseName) {
      result = result.filter(function (element, index, array) {
        return element.chinese_name.indexOf(keys.courseName) >= 0;
      });
    }

    if(keys.teacherName) {
      result = result.filter(function (element, index, array) {
        return element.teacher.indexOf(keys.teacherName) >= 0;
      });
    }

    this.setState({result: result});
  },
  handleCourseAdd: function(course) {
    /**
     * Data Obj format: (column name)
     * course uid
     * Course Code
     * Course Name
     * Teacher Name
     * Time
     */
    this.props.handleAddCourse({
      courseUid:course.uid,
      courseCode:course.code,
      courseName:course.chinese_name,
      teacherName:course.teacher,
      courseTime:course.time.split(',').map(function(element) { return parseInt(element) })
    })
  },
  render: function() {
    if (!this.state.courseData) return null;

    return (
      <div className="ui grid stackable">
        <div className="six wide column">
          <SearchForm degree={this.state.degree}
            department={this.state.courseData.department}
            updateTime={this.state.courseData.update}
            handleSubmit={this.handleSearchFormSubmit} />
        </div>

        <div className="ten wide column searchResult">
          <SearchResult result={this.state.result}
            handleAdd={this.handleCourseAdd} />
        </div>

      </div>
    )
  }
});

var SearchForm = React.createClass({
  getInitialState: function() {
    return({
      department: 0,
      degree: 0
    })
  },
  handleDepartmentChange: function(value) {
    if(value) this.setState({department: value});
  },
  handleGradeChange: function(value) {
    if(value) this.setState({degree: value});
  },
  handleReset: function() {
    $('form').removeClass('error');
    if(this.state.department != 0) {
      $('.dropdown.department')
        .dropdown('restore defaults')
      ;
    }

    if(this.state.degree != 0) {
      $('.dropdown.degree')
        .dropdown('restore defaults')
      ;
    }

  },
  handleSubmit: function(e) {
    $('form').removeClass('error');
    e.preventDefault();
    var keys = {
      department: this.state.department,
      degree: this.state.degree,
      courseCode: (React.findDOMNode(this.refs.courseCode).value.trim() || null),
      courseName: (React.findDOMNode(this.refs.courseName).value.trim() || null),
      teacherName: (React.findDOMNode(this.refs.teacherName).value.trim() || null)
    }

    if( keys.department != 0
       || keys.degree != 0
       || keys.courseCode
       || keys.courseName
       || keys.teacherName)
      this.props.handleSubmit(keys);
    else
      $('form').addClass('error');
  },
  render: function() {
    var Department = this.props.department.map(function(element, index) {
      return (<option key={index + 1} value={element.departmentCode}>{element.departmentName}</option>)
    });
    Department.unshift(<option key={0} value={0}>請選擇 Please Select</option>)

    var Grade = this.props.degree.map(function(element, index) {
      return (<option key={index + 1} value={element}>{element}</option>)
    });
    Grade.unshift(<option key={0} value={0}>請選擇 Please Select</option>)

    return (
      <form className="ui form" onSubmit={this.handleSubmit}>
        <h2 className="ui dividing header">搜尋課程</h2>
          <div className="ui error message">
            <div className="header">缺少搜尋條件</div>
            <p>請至少指定一個搜尋條件，再進行搜尋。</p>
          </div>
          <div className="field">
            <label>開課系所 Department</label>
            <select defaultValue={this.state.department} className="ui dropdown search department">
              {Department}
            </select>
          </div>
          <div className="field">
            <label>選課年級 Grade</label>
            <select defaultValue={this.state.degree} className="ui dropdown degree">
              {Grade}
            </select>
          </div>
          <div className="field">
            <label>課號</label>
            <input type="text" placeholder="Course Code" ref="courseCode" />
          </div>
          <div className="field">
            <label>課程名稱</label>
            <input type="text" placeholder="Course Name" ref="courseName" />
          </div>
          <div className="field">
            <label>開課教師</label>
            <input type="text" placeholder="Teacher Name" ref="teacherName" />
          </div>
          <div className="field">
            <label>資料庫最後更新時間</label>{this.props.updateTime}
          </div>
          <div className="ui buttons right floated">
            <button type="reset" className="ui button reset" onClick={this.handleReset}>Reset</button>
            <div className="or"></div>
            <button type="submit" className="ui positive button">Search</button>
          </div>
      </form>
    )
  },
  componentDidMount: function() {
    $('select.dropdown.department')
      .dropdown({
        onChange: this.handleDepartmentChange
      })
    ;
    $('select.dropdown.degree')
      .dropdown({
        onChange: this.handleGradeChange
      })
    ;
  }
})

var SearchResult = React.createClass({
  handleAdd: function(course) {
    this.props.handleAdd(course);
  },
  render: function() {
    if(!this.props.result) return null;
    var result = this.props.result.map(function(element, index) {
      return(
        <tr key={index}>
          <td><a href={element.url} target="_blank">{element.code}</a></td>
          <td>{element.teacher}</td>
          <td>{element.chinese_name}</td>
          <td>{element.credit}</td>
          <td>{element.time}</td>
          <td>{element.degree}</td>
          <td><div className="ui basic olive button" onClick={this.handleAdd.bind(this, element)}>Add</div></td>
        </tr>
      )
    }.bind(this));

    return (
      <div className="ui segment">
        <div className="ui dimmer">
          <div className="ui indeterminate text loader">Searching</div>
        </div>
        <table className="ui very basic collapsing celled table">
          <thead>
            <tr>
              <th className="one wide">課號</th>
              <th className="two wide">開課教師</th>
              <th className="three wide">課程名稱</th>
              <th className="one wide">學分</th>
              <th className="one wide">時間</th>
              <th className="one wide">可選年級</th>
              <th className="one wide">Add</th>
            </tr>
          </thead>
          <tbody>
            {result}
          </tbody>
        </table>
      </div>
    )
  }
});

$(document).ready(function() {
  $('.menu .item')
    .tab()
  ;
});
