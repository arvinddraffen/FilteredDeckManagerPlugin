## Configuration Options
### `allow_empty`
Create a filtered deck even if it will have no cards.

---

### `reschedule`
Enable the option to reschedule cards when answered in the filtered deck.

---

### `intervals`
* `again`
    * Interval (in seconds) to use when pressing the `again` key
* `hard`
    * Interval (in seconds) to use when pressing the `hard` key
* `good`
    * Interval (in seconds) to use when pressing the `good` key

---

### `orders`
* `order_by_search1`
* `order_by_search2`

Set the ordering to use for the searches used for filtered deck generation. Values should be a number, based on the following:
<!-- Table extension not enabled for markdown.extensions md_in_html.

| Order Type | Value|
| ---------- | ---- |
| Oldest Seen First | 0 |
| Random | 1 |
| Increasing Intervals | 2 |
| Decreasing Intervals | 3 |
| Most Lapses | 4 |
| Order Added | 5 |
| Order Due | 6 |
| Last Added First | 7 |
| Relative Overdueness | 8 |

-->

* Oldest Seen First: 0
* Random: 1
* Increasing Intervals: 2
* Decreasing Intervals: 3
* Most Lapses: 4
* Order Added: 5
* Order Due: 6
* Last Added First: 7
* Relative Overdueness: 8

---

### `card_limit`
The maximum number of cards to use on filtered deck creation.

---

**Note**: Restart Anki for add-on changes to take effect.
