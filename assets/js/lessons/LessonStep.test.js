import React from 'react'
import LessonStep from './LessonStep'
import { mount, shallow } from 'enzyme'

describe('LessonStep', () => {
  const step = {
    html: '<p>This is</p><p>a <em>step</em></p>',
    highlight: [ { type: 'EditableNotes' } ],
  }

  it('renders the description HTML', () => {
    const wrapper = shallow(<LessonStep {...step} />)
    expect(wrapper.find('.description').html()).toEqual('<div class="description"><p>This is</p><p>a <em>step</em></p></div>')
  })
})