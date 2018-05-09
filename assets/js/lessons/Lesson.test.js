import React from 'react'
import Lesson from './Lesson'
import { mount, shallow } from 'enzyme'
import configureStore from 'redux-mock-store'

describe('Lesson', () => {
  const lesson = {
    slug: 'a-lesson',
    header: {
      title: 'Lesson Title',
      html: '<p>Lesson HTML</p>',
    },
    sections: [
      {
        title: 'Section One',
        html: '<p>Section One HTML</p>',
        steps: [
          { html: 'Step One-Ay', highlight: [ { type: 'EditableNotes' } ] },
          { html: 'Step One-<strong>Bee</strong>', highlight: [ { type: 'WfModule', name: 'Foo' } ] },
        ],
      },
      {
        title: 'Section Two',
        html: '<p>Section Two HTML</p>',
        steps: [
          { html: 'Step Two-Ay', highlight: [ { type: 'EditableNotes' } ] },
          { html: 'Step Two-<strong>Bee</strong>', highlight: [ { type: 'WfModule', name: 'Foo' } ] },
        ],
      },
      {
        title: 'Last Section',
        html: '<p>Section Three HTML</p>',
        steps: [
          { html: 'Step Three-Ay', highlight: [ { type: 'EditableNotes' } ] },
          { html: 'Step Three-<strong>Bee</strong>', highlight: [ { type: 'WfModule', name: 'Foo' } ] },
        ],
      },
    ],
  }

  describe('shallow', () => {
    const wrapper = () => {
      const store = configureStore()({ lesson_highlight: [] })
      return shallow(<Lesson store={store} {...lesson} />).dive()
    }

    it('renders a title', () => {
      expect(wrapper().find('h1').text()).toEqual('Lesson Title')
    })

    it('renders the description HTML', () => {
      expect(wrapper().find('.description').html()).toEqual('<div class="description"><p>Lesson HTML</p></div>')
    })

    it('renders LessonSections', () => {
      expect(wrapper().find('LessonSection')).toHaveLength(3)
    })

    it('sets the first Lesson active', () => {
      expect(wrapper().find('LessonSection').map(s => s.props().active)).toEqual([ true, false, false ])
    })
  })

  describe('navigation', () => {
    // integration-test-y: this tests that Lesson, LessonNav and LessonSection
    // all work together to track the active section.

    let store
    const wrapper = () => {
      store = configureStore()({ lesson_highlight: [] })
      return mount(<Lesson store={store} {...lesson} />)
    }

    it('shows "Next" and an unclickable "Previous"', () => {
      const w = wrapper()
      expect(w.find('footer button[name="Previous"]').nodes[0].disabled).toEqual(true)
      expect(w.find('footer .active').text()).toEqual('1 of 3')
      expect(w.find('section').map(n => n.node.className)).toEqual([ 'active', 'inactive', 'inactive' ])
      expect(w.find('footer button[name="Next"]').nodes[0].disabled).toEqual(false)
    })

    it('moves to the next section', () => {
      const w = wrapper()
      w.find('footer button[name="Next"]').simulate('click')
      expect(w.find('footer button[name="Previous"]').nodes[0].disabled).toEqual(false)
      expect(w.find('footer .active').text()).toEqual('2 of 3')
      expect(w.find('section').map(n => n.node.className)).toEqual([ 'inactive', 'active', 'inactive' ])
      expect(w.find('footer button[name="Next"]').nodes[0].disabled).toEqual(false)
    })

    it('disables Next on the final section', () => {
      const w = wrapper()
      w.find('footer button[name="Next"]').simulate('click').simulate('click')
      expect(w.find('footer button[name="Previous"]').nodes[0].disabled).toEqual(false)
      expect(w.find('footer .active').text()).toEqual('3 of 3')
      expect(w.find('section').map(n => n.node.className)).toEqual([ 'inactive', 'inactive', 'active' ])
      expect(w.find('footer button[name="Next"]').nodes[0].disabled).toEqual(true)
    })

    it('dispatches store.setLessonHighlight', () => {
      const w = wrapper()
      expect(store.getActions()).toEqual([
        { type: 'SET_LESSON_HIGHLIGHT', payload: [ { type: 'EditableNotes' } ] },
      ])
    })
  })
})