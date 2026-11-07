Page({
  data: { itemType: 'FOOD' },
  changeType(event) {
    const itemType = event.currentTarget.dataset.type;
    if (itemType === 'FOOD' || itemType === 'MEDICINE') this.setData({ itemType });
  },
});
